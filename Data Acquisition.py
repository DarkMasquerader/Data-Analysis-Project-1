'''
This Python script is responsible for the acquisition, transformation, and exporting of the data needed for this project.
'''

# Web scraping libraries
from bs4 import BeautifulSoup
import requests

# Web interaction/botting libraries 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

# General libraries
import pickle
import time
import os

# Dataframe library
import pandas as pd
# myDataFrame = pd.DataFrame(columns = ['Rank', 'Game Title', 'Date', 'Avg. Players', 'Peak Players'])

# Global vars
isCollectingNewData = True
url_steamChartsBase = 'https://steamcharts.com'
io_path = f'../Data Analysis- Are F2P Games the Solomn Future/list_of_games_data.pkl'
list_of_games = []
list_game_url = []

def main():

    '''
    This function is used to determine if new data is going to be scraped, or loaded from local memory.
    '''
    determineCollectNewData()

    '''
    In this function, the basic details of each game are acquired: popularity ranking, game title, and game Steam Charts URL.
    
    The URL is acquired due to a game URL being determined by an unpredictable, randomly assigned number.

    This information enables the automated scraping of the required data from this website, in the getGameStats() function.
    '''
    getSteamChartsGameList()
        
    '''
    In this function, statistical details for each game are acquired and stored in a Game object.

    The end result is a list of Game objects enabling data to be easily added to a dataframe and exported.
    '''
    getGameStats()

    '''
    In this function, a bot is created to interact with Steam's official site to get the current price of the game. 

    The bot is designed to handle 'unexpected' pages and varying page layouts.
    '''
    getGamePrices()

    # Read/write variables locally
    handleVariables()
        
        
        
# My Functions
def handleVariables():
    global list_of_games
    if isCollectingNewData:
        with open('list_of_games_data.pkl', 'wb') as f:
            pickle.dump(list_of_games, f)
    elif not isCollectingNewData:
        with open(io_path, 'rb') as f:
            list_of_games = pickle.load(f)
    

def determineCollectNewData():
    if os.path.exists(io_path):
        global isCollectingNewData
        isCollectingNewData = False

def getHTML(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, "html")

def getTableColumns(pageText):
    dirtyTable = pageText.find('table')
    dirtyHeaders = dirtyTable.find_all('th')
    return dirtyTable, dirtyHeaders

def getSteamChartsGameList():

    # Base Case
    if not isCollectingNewData:
        return 

    for pageCounter in range(1,2):

        # Acquire HTML
        url_steamChartsCurrent = f"{url_steamChartsBase}/top/p.{pageCounter}"
        pageText_steamCharts = getHTML(url_steamChartsCurrent)

        # Isolate table columns
        dirtyTable, dirtyHeaders = getTableColumns(pageText_steamCharts)

        # Acquire: Rank, Name, URL
        tableRows = dirtyTable.find_all('tr')
        for row in tableRows[1:]: #tableRows[0] contains column titles
            linkTag = row.find('a')
            link = linkTag.get('href') # Isolate URL component for next for loop
            gameTitle = linkTag.text.strip() # Isolate game title
            list_game_url.append((tableRows.index(row),gameTitle, link))

def getGameStats():

    # Base Case
    if not isCollectingNewData:
        return 

    for gameInfo in list_game_url:
        
        # Create Game Object 
        tempGameObject = Game(gameInfo[1], gameInfo[0])

        # Acquire HTML
        url_steamChartGame = f"{url_steamChartsBase}{gameInfo[2]}"
        pageText_steamChartGame = getHTML(url_steamChartGame)

        # Isolate table columns
        dirtyTable, dirtyHeaders = getTableColumns(pageText_steamChartGame)
        
        # Get row data
        tableRows = dirtyTable.find_all('tr')
        for row in tableRows[1:]: #tableRows[0] contains column titles
            row_data = row.find_all('td')
            list_of_row_data = [data.text.strip() for data in row_data]

            # Add data to Game object 
            tempGameObject.add_entry(list_of_row_data[0], list_of_row_data[1], list_of_row_data[4]) 

        # Add Game object to list 
        list_of_games.append(tempGameObject)

def getGamePrices(list_of_games):

    # Base Case
    if not isCollectingNewData:
        return 

    # Setup chrome driver
    service = Service(executable_path=f'../Data Analysis- Are F2P Games the Solomn Future/chromedriver')
    driver = webdriver.Chrome(service=service)
    
    # For each game, get price (game name, price)
    for game in list_of_games:
        gameTitle = game.get_name()

        # Open site 
        driver.get('https://store.steampowered.com/')

        # Safely confirm presence of textbox
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'store_nav_search_term'))
        )

        # Identify and interact with textbox
        input_element = driver.find_element(By.ID, 'store_nav_search_term')       
        input_element.send_keys(gameTitle + Keys.ENTER)

        # Isolate Steam page URL
        pageHTML = driver.page_source
        url_index = pageHTML.find('store.steampowered.com/app')
        messyURL = pageHTML[url_index:url_index + 200]
        cleanURL  = '/'.join(messyURL.split('/')[:4]) + '/'


        # Go to Steam page and get price
        driver.get(f'https://{cleanURL}')
        
        # Handle age verification
        if 'agecheck' in driver.current_url:
            
            # Select birth year as 2000
            dropdown = driver.find_element(By.ID, 'ageYear')
            select = Select(dropdown)
            select.select_by_value('2000')

            # Click 'View Page' button
            button = driver.find_element(By.ID, 'view_product_page_btn')
            button.click()

            # Wait for page to load
            time.sleep(2)

        
        # Identify price
        pageHTML = driver.page_source
        
        cleanPrice = None
        try:
            dirtyPrice = driver.find_element(By.CLASS_NAME, 'game_purchase_price')
            cleanPrice = dirtyPrice.text
        except NoSuchElementException:
            dirtyPrice = driver.find_element(By.CLASS_NAME, 'discount_final_price')
            cleanPrice = dirtyPrice.text
        
        # Update Price
        game.set_price('£0' if cleanPrice == 'Free to Play' or cleanPrice == 'Free' else cleanPrice)

    driver.quit()

# My Classes
class Game:

    def __init__(self, name, rank):
        self.title = name
        self.rank = rank
        self.list_month = []
        self.list_avg = []
        self.list_peak = []
        self.price = None

    def add_entry(self, month, avg, peak):
        self.list_month.append(month)
        self.list_avg.append(avg)
        self.list_peak.append(peak)

    def get_name(self):
        return self.title

    def set_price(self, price):
        self.price = price

    '''
    Returns a list with each row containing the x-th value from each of the lists.
    NOTE: The return value needs to be iterated by row to be passed into the dataframe
    '''
    def to_list(self):
        self.return_list = []
        for pos in range(len(self.list_month)):
            self.return_list.append([self.list_month[pos], self.list_avg[pos], self.list_peak[pos]])
        
        return self.return_list

# Main Loop
if __name__ == '__main__':
    main()