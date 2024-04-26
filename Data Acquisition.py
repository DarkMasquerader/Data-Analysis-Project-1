'''
This Python script is responsible for the acquisition, transformation, and exporting of the data needed for this project.
'''

# Web scraping libraries
from bs4 import BeautifulSoup
import requests

# Dataframe library
import pandas as pd
# myDataFrame = pd.DataFrame(columns = ['Rank', 'Game Title', 'Date', 'Avg. Players', 'Peak Players'])

def main():

    #Acquire top 100 games 
    url_steamChartsBase = 'https://steamcharts.com'

    # Create list of games and URLs
    list_game_url = []

    # For each page, get list of games
    for pageCounter in range(1,2):

        # Acquire HTML
        url_steamChartsCurrent = f"{url_steamChartsBase}/top/p.{pageCounter}"
        pageText_steamCharts = getHTML(url_steamChartsCurrent)

        # Isolate table columns
        dirtyTable, dirtyHeaders = getTableColumns(pageText_steamCharts)

        # Acquire: Rank, Name, URL
        tableRows = dirtyTable.find_all('tr')
        for row in tableRows[1:]:
            linkTag = row.find('a')
            link = linkTag.get('href') # Isolate URL component for next for loop
            gameTitle = linkTag.text.strip() # Isolate game title
            list_game_url.append((tableRows.index(row),gameTitle, link))
        
    # For each game, get information (date, avg. players, peak players)
    for game in list_game_url:
        
        # Acquire HTML
        url_steamChartGame = f"{url_steamChartsBase}{game[2]}"
        pageText_steamChartGame = getHTML(url_steamChartGame)

        # Isolate Table columns
        dirtyTable, dirtyHeaders = getTableColumns(pageText_steamChartGame)

    # For each game, get price (game name, price)
        
        

def getHTML(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, "html")

def getTableColumns(pageText):
    dirtyTable = pageText.find('table')
    dirtyHeaders = dirtyTable.find_all('th')

if __name__ == '__main__':
    main()


class Games:

    def __init__(self):
        self.list_month = []
        self.list_avg = []
        self.list_peak = []

    def add_entry(self, month, avg, peak):
        self.list_month.append(month)
        self.list_avg.append(avg)
        self.list_peak.append(peak)


    '''
    Returns a list with each row containing the x-th value from each of the lists.
    The output of this function is used as input to a dataframe.
    NOTE: The return value needs to be iterated by row to be passed into the dataframe
    '''
    def to_list(self):
        self.return_list = []
        for pos in range(len(self.list_month)):
            self.return_list.append([self.list_month[pos], self.list_avg[pos], self.list_peak[pos]])
        
        return self.return_list
