# Data Acquisition
This directory contains three files, `chromedriver`, `Data Acquisition.py`, and `MyGameClass.py`.

`chromedriver` is the MAC/Linux executable required for website automation.

`Data Acquisition.py` is the script used for collecting and processing data.

`MyGameClass.py` contains the class used to handle the data for each game included in the analysis.

## Script Structure
The main loop is well-commented, providing a high-level explanation of the script.
The main loop is included in-line, below.

```Python
def main():

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
    In this function, a bot is created to interact with Steam's official site to get the current price of the game,
    alongside other miscellaneous information. 
    The bot is designed to handle 'unexpected' and inconsistent page layouts.
    '''
    getGameInfoFromSteamThreaded() if isThreading else getGameInfoFromSteam()

    # Read/write variables locally
    handleVariables()
    
    '''
    In this function, the collected data is handled and exported into two .csv files for subsequent data analysis.
    '''
    handleExport()
```

## Threads and Mutexes
This script partially executes in a multi-threaded environment, to speed up the data acquisition process.

With threads having access to shared memory, concurrent access to shared resources (i.e. variables) needs to be handled to prevent unpredictable outcomes.
Mutexes, as shown below, have been employed to ensure safe access to shared resources.

```Python
from threading import Thread, Lock
threadLimit = 15 # Set thread limit
isThreading = True # Set to false to run on single thread
mutex = Lock()

...

def getNextGame():
    with mutex:
        global threadGameCounter
        threadGameCounter += 1
        return next(threadGameList), threadGameCounter, 
```