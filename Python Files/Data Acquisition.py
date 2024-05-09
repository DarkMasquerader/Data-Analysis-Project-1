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
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# General libraries
import pickle
import time
import os

# Dataframe library
import pandas as pd

# Threading libraries
from threading import Thread, Lock
threadLimit = 15 # Set thread limit
isThreading = True # Set to false to run on single thread
mutex = Lock()

# Global vars
no_games = 200 # Choose number of games to sample
no_pages =  (no_games // 25) + 2
max_games = 25 * (no_pages-1)

list_of_games = []
list_game_url = []

isCollectingNewData = None
url_steamChartsBase = 'https://steamcharts.com'

# I/O Vars
dataset = '912 Samples' # 912 - 244
io_path = f'./Datasets/{dataset}/list_of_games_data.pkl'

def main():

    # Path Testing
    # print(f'CWD: {os.getcwd()}')
    # print(f'Path: {io_path}')
    # print(f'Path: {os.path.exists(io_path)}')
    # return

    '''
    This function is used to determine if new data is going to be scraped, 
    or if previously scraped data will be will be loaded from local memory.
    '''
    determineCollectNewData()

    '''
    In this function, the basic details of each game are acquired: popularity ranking, game title, and game Steam Charts URL.
    The URL is acquired due to a game's URL being determined by an unpredictable, randomly assigned number.
    This information enables the automated scraping of the required data from SteamCharts, in the getGameStats() function.
    '''
    getSteamChartsGameList()
        
    '''
    In this function, statistical details for each game are acquired from SteamCharts and stored in a Game object.
    The end result is a list of Game objects enabling data to be easily added to a dataframe and exported.
    '''
    getGameStats()

    '''
    In this function, a bot is created to interact with Steam's official site to get the current price of the game, alongside other miscellaneous information. 
    The bot is designed to handle 'unexpected' and inconsistent page layouts.
    '''
    getGameInfoFromSteamThreaded() if isThreading else getGameInfoFromSteam()

    # Read/write variables locally
    handleVariables()
    
    # Export to .csv
    handleExport()
    
# Thread Functions 
threadGameCounter = 0
def getNextGame():
    with mutex:
        global threadGameCounter
        threadGameCounter += 1
        return next(threadGameList), threadGameCounter, 

def threadCallee(num):

    print(f'Thread #{num} started')
    
    # Setup chrome driver
    service = Service(executable_path=f'../Data Analysis- Are F2P Games the Solomn Future/chromedriver')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # For each game, get price (game name, price)
        
    while True:
        try:
            game, gameNumber = getNextGame()
            # Get game title
            gameTitle = game.get_name()
            
            # Debug print
            print(f"({gameNumber}/{max_games}) Current Game: {gameTitle} <Thread #{num}>")

            # Open homepage 
            driver.get('https://store.steampowered.com/')
            # driver.minimize_window()

            # Safely confirm presence of textbox before attempting interaction
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'store_nav_search_term'))
            )

            # Identify and interact with textbox (searching for steam game)
            input_element = driver.find_element(By.ID, 'store_nav_search_term')       
            input_element.send_keys(gameTitle + Keys.ENTER)

            # Isolate Steam search page URL
            pageHTML = driver.page_source
            
            # Base Case - Game not found
            if '0 results match your search.' in pageHTML:
                list_of_games.remove(game) # Remove game
                continue # Go to next game in list
            else:
                url_index = pageHTML.find('store.steampowered.com/app')
                messyURL = pageHTML[url_index:url_index + 200]
                cleanURL  = '/'.join(messyURL.split('/')[:4]) + '/'

            # Go to Steam page and get price
            driver.get(f'https://{cleanURL}')
            
            # Base Case - Age verification page
            handleAgeVerificationPage(driver)

            # Identify price
            isolateGamePrice(game, driver)

            # Identify features
            isolateGameFeatures(game, driver)

            # time.sleep(4)

        except ValueError as e:
            print(f'Exception Occurred: {e}')
            continue
        except NoSuchElementException as e:
            print(f'Exception Occurred: {e}')
            continue
        except TimeoutException as e:
            print(f'Timeout on game: {gameTitle} (Thread #{num})\n{e}')
            continue
        except StopIteration:
            print('End of list')
            driver.quit()
            break

def getGameInfoFromSteamThreaded():
    
    # Base Case - Are reading in or collecting new data?
    if not isCollectingNewData:
        return 

    # Recording running time
    start_time = time.time()

    global threadGameList
    threadGameList = iter(list_of_games)

    _list = []
    for temp in range(0,threadLimit):
        _ = Thread(target = threadCallee, args = [temp,] )
        _.start()
        _list.append(_)

    for _ in _list:
        _.join()

    # Display running time
    end_time = time.time()
    print(f'Steam Runtime: {end_time-start_time}')

# Scraping Functions
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

def getGameInfoFromSteam():

    # Base Case - Are reading in or collecting new data?
    if not isCollectingNewData:
        return 

    # Recording running time
    start_time = time.time()

    # Setup chrome driver
    service = Service(executable_path=f'../Data Analysis- Are F2P Games the Solomn Future/chromedriver')
    # global driver
    driver = webdriver.Chrome(service=service)
    
    # For each game, get price (game name, price)
    _counter = 0
    for game in list_of_games:
        
        try:
            # Get game title
            gameTitle = game.get_name()
            
            # Debug print
            _counter += 1
            print(f"({_counter}/{max_games}) Current Game: {gameTitle}")

            # Open homepage 
            driver.get('https://store.steampowered.com/')

            # Safely confirm presence of textbox before attempting interaction
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'store_nav_search_term'))
            )

            # Identify and interact with textbox (searching for steam game)
            input_element = driver.find_element(By.ID, 'store_nav_search_term')       
            input_element.send_keys(gameTitle + Keys.ENTER)

            # Isolate Steam search page URL
            pageHTML = driver.page_source
            
            # Base Case - Game not found
            if '0 results match your search.' in pageHTML:
                list_of_games.remove(game) # Remove game
                continue # Go to next game in list
            else:
                url_index = pageHTML.find('store.steampowered.com/app')
                messyURL = pageHTML[url_index:url_index + 200]
                cleanURL  = '/'.join(messyURL.split('/')[:4]) + '/'

            # Go to Steam page and get price
            driver.get(f'https://{cleanURL}')
            
            # Base Case - Age verification page
            handleAgeVerificationPage(driver)

            # Identify price
            isolateGamePrice(game, driver)

            # Identify features
            isolateGameFeatures(game, driver)

        except ValueError as e:
            print(f'Exception Occurred: {e}')
            continue

    driver.quit()

    # Display running time
    end_time = time.time()
    print(f'Steam Runtime: {end_time-start_time}')

def isolateGamePrice(game, driver):
        try:

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'game_purchase_price'))
            )

            dirtyPrice = driver.find_element(By.CLASS_NAME, 'game_purchase_price')
            cleanPrice = dirtyPrice.text.lower().strip()
        except TimeoutException:

            try:
                dirtyPrice = driver.find_element(By.CLASS_NAME, 'discount_final_price')
                cleanPrice = dirtyPrice.text.lower().strip()
            
            except NoSuchElementException:
                print(f'No price found for: {game.get_name}')
                game.set_price('NULL')
                return

        # Update Price
        game.set_price('£0' if 'free' in cleanPrice else cleanPrice)

def getHTML(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, "html")

def getSteamChartsGameList():

    # Base Case
    if not isCollectingNewData:
        return 

    rankCounter = 1
    for pageCounter in range(1, no_pages):

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
            list_game_url.append((rankCounter,gameTitle, link))
            rankCounter += 1

def handleAgeVerificationPage(driver):
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

# I/O Functions
def handleVariables():
    global list_of_games
    if isCollectingNewData:
        with open('list_of_games_data.pkl', 'wb') as f:
            pickle.dump(list_of_games, f)
    elif not isCollectingNewData:
        with open(io_path, 'rb') as f:
            list_of_games = pickle.load(f)
    
def determineCollectNewData():
    global isCollectingNewData
    if os.path.exists(io_path):
        isCollectingNewData = False
    else:
        isCollectingNewData = True

def handleExport():
    # Create dataframes
    statsDataFrame = pd.DataFrame(columns = ['Game Title', 'Rank', 'Date', 'Avg. Players', 'Peak Players'])
    detailsDataFrame = pd.DataFrame(columns= ['Game Title', 'Price', 'Single Player', 'Online PvP', 'Online Co-Op', 'In-App Purchases', 'Tags'])
        
    my_global_tag_set = set()

    # Fill dataframes
    for game in list_of_games:

        for row in game.to_stats_list():
            statsDataFrame.loc[len(statsDataFrame)] = row
        
        detailsDataFrame.loc[len(detailsDataFrame)] = game.to_details()

        # Build list of unique tags
        my_global_tag_set.update(game.get_tags())
    
    # Create and fill tags dataframe
    list_of_unique_tags = list(my_global_tag_set) # Placed in list to guarantee order
    dataframe_columns = ['Game Title']
    dataframe_columns += list_of_unique_tags
    tagsDataFrame = pd.DataFrame(columns=dataframe_columns)
    for game in list_of_games:
        row = [] # Row to add to dataframe
        row.append(game.get_name()) 
        cur_game_tags = game.get_tags()

        # For each tag, check if it's present
        for tag in list_of_unique_tags: 
            if tag in cur_game_tags:
                row.append(True)
            else:
                row.append(False)
        
        tagsDataFrame.loc[len(tagsDataFrame)] = row

    statsDataFrame.to_csv('Stats.csv', index = False)
    detailsDataFrame.to_csv('Details.csv', index = False)
    tagsDataFrame.to_csv('Tags.csv', index=False)

# Data Manipulation Functions
def getTableColumns(pageText):
    dirtyTable = pageText.find('table')
    dirtyHeaders = dirtyTable.find_all('th')
    return dirtyTable, dirtyHeaders

def isolateGameFeatures(game, driver):
    list_of_features = ('In-App Purchases', 'Online PvP', 'Online Co-op', 'Single-player', 'Cross-Platform Multiplayer')

    # Get page HTML
    pageHTML = driver.page_source

    # Set tag field in class object for each tag found
    for feature in list_of_features:
        if f'<div class="label">{feature}</div>' in pageHTML:
            match feature:
                case 'In-App Purchases':
                    game.set_in_app_purchase()
                case 'Online PvP', 'Cross-Platform Multiplayer':
                    game.set_pvp()
                case 'Online Co-op':
                    game.set_coop()
                case 'Single-player':
                    game.set_1p()

    # Awkward cases
    elements = driver.find_elements(By.CLASS_NAME, 'app_tag')
    for e in elements:
        if 'Multiplayer' in e.text:
            game.set_pvp()
        
        game.add_tag_to_set(e.text)

    return
        
# My Classes
class Game:

    '''
    This class is used to represent each game included in this analysis, and provides an easy means of exporting this data to a DataFrame and .csv.
    '''

    def __init__(self, name, rank):
        self.title = name
        self.rank = rank
        self.list_month = []
        self.list_avg = []
        self.list_peak = []
        self.tag_set = set()
        self.price = None
        self.has_in_app_purchase = False
        self.has_online_pvp = False
        self.has_online_co_op = False
        self.has_single_player = False

    def add_entry(self, month, avg, peak):
        self.list_month.append(month)
        self.list_avg.append(avg)
        self.list_peak.append(peak)

    def get_name(self):
        return self.title

    def set_price(self, price):
        # self.price = price
        self.price = 'NULL' if "£" not in price else price

    def set_in_app_purchase(self):
        self.has_in_app_purchase = True

    def set_pvp(self):
        self.has_online_pvp = True
    
    def set_coop(self):
        self.has_online_co_op = True
    
    def set_1p(self):
        self.has_single_player = True

    def add_tag_to_set(self, tag):
        self.tag_set.add(tag)

    def get_tags(self):
        return self.tag_set

    '''
    Returns a nested list with each row containing the x-th value from each of the lists.
    Structure: Title, Rank, Month, Average Peak
    NOTE: The return value needs to be iterated by row to be passed into the dataframe
    '''
    def to_stats_list(self):
        self.return_list = []
        for pos in range(len(self.list_month)):
            self.return_list.append([self.title, self.rank, self.list_month[pos], self.list_avg[pos], self.list_peak[pos]])
        
        return self.return_list

    '''
    Returns a list of details for the dataframe showing the information of the game stored on Steam's website
    '''
    def to_details(self):
        if self.price is None or '£' not in self.price:
            self.price = '£0'

        # Removing junk values identified post-data collection
        self.tag_set.discard('')
        self.tag_set.discard('+')

        return [self.title, self.price, self.has_single_player, self.has_online_pvp, self.has_online_co_op, self.has_in_app_purchase, [x for x in self.tag_set]]

# Main Loop
if __name__ == '__main__':
    main()