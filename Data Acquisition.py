'''
This Python script is responsible for the acquisition, transformation, and exporting of the data needed for this project.
'''

# Web scraping libraries
from bs4 import BeautifulSoup
import requests

# Web interaction libraries 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# General libraries
import pickle
import time
import os

# Dataframe library
import pandas as pd
# myDataFrame = pd.DataFrame(columns = ['Rank', 'Game Title', 'Date', 'Avg. Players', 'Peak Players'])

isCollectingNewData = True
io_path = f'../Data Analysis- Are F2P Games the Solomn Future/list_of_games_data.pkl'

def main():

    url_steamChartsBase = 'https://steamcharts.com'

    # Scraping or reading in data?
    determineCollectNewData()

    '''
    In this function, the basic details of each game are acquired: popularity ranking, game title, and game Steam Charts URL.
    
    The URL is acquired due to a game URL being determined by an unpredictable, randomly assigned number.

    This information enables the automated scraping of the required data from this website, in the getGameStats() function.
    '''
    list_game_url = []
    getSteamChartsGameList(list_game_url, url_steamChartsBase)
        
    '''
    In this function, statistical details for each game are acquired and stored in a Game object.

    The end result is a list of Game objects enabling data to be easily added to a dataframe and exported.
    '''
    list_of_games = []
    getGameStats(list_game_url, url_steamChartsBase, list_of_games)

    # Reading/writing variables locally
    list_of_games = handleVariables(list_of_games)

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
            #todo

        pageHTML = driver.page_source
        price_index = pageHTML.find('game_purchase_price')
        messyPrice = pageHTML[price_index:price_index + 200]
        cleanPrice = messyPrice.split('>')[1].split('<')[0].strip()
        
        # Update Price
        game.set_price('£0' if cleanPrice == 'Free to Play' else cleanPrice)

        # https://store.steampowered.com/app/271590/Grand_Theft_Auto_V/ - Problem game

    isCollectingNewData = True
    handleVariables(list_of_games)
    input()
        
        
        
# My Functions
def handleVariables(list_of_games):
    if isCollectingNewData:
        with open('list_of_games_data.pkl', 'wb') as f:
            pickle.dump(list_of_games, f)
    elif not isCollectingNewData:
        with open(io_path, 'rb') as f:
            list_of_games = pickle.load(f)
    
    return list_of_games

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

def getSteamChartsGameList(list_game_url, url_steamChartsBase):

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

def getGameStats(list_game_url, url_steamChartsBase, list_of_games):

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