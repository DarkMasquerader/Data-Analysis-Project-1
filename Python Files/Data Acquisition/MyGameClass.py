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
        Description
        ------------
        Returns a nested list with each row containing the x-th value from each of the lists [Structure: Title, Rank, Month, Average Peak]

        NOTE: The return value needs to be iterated by row to be passed into the DataFrame object.
        
        Parameters
        ----------
        This function does not take any parameters.
        
        Returns
        -------
        self.return_list: list
            A list containing containing the row-values (Title, Rank, Month, Average Peak) for each game.
        
        Raises
        ------
        This function does not raise any exceptions.
    '''
    def to_stats_list(self):
        self.return_list = []
        for pos in range(len(self.list_month)):
            self.return_list.append([self.title, self.rank, self.convert_to_date(self.list_month[pos]), self.list_avg[pos], self.list_peak[pos]])
        
        return self.return_list
    
    '''
        Description
        ------------
        This function converts the scraped date into a format that can be handled by Tableau.
    
        Parameters
        ----------
        date: str
            This is the text representation fo the date scraped from SteamCharts.
    
        Returns
        -------
        _: str
            A textual representation of the date in a format that can be processed by Tableau.
    
        Raises
        ------
        This function does not raise any exceptions.
    '''
    month_to_number = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    def convert_to_date(self, date):
        split_date = date.split(' ')
        
        if len(split_date) == 3: # Value: Last 30 Days
            return '5-2024' #Naughty hard-coded value
        else:
            return f'{Game.month_to_number[split_date[0]]}-{split_date[1]}'

    '''
        Description
        ------------
        Returns a list of details for the DataFrame object which contains the information available for a game on the Steam website.
    
        Parameters
        ----------
        This function does not take any parameters.
    
        Returns
        -------
        _: list
            A list containing the details scraped from Steam.
    
        Raises
        ------
        This function does not raise any exceptions.
    '''
    def to_details(self):
        if self.price is None or '£' not in self.price:
            self.price = '£0'

        # Removing junk values identified post-data collection
        self.tag_set.discard('')
        self.tag_set.discard('+')

        return [self.title, self.price, self.has_single_player, self.has_online_pvp, self.has_online_co_op, self.has_in_app_purchase, [x for x in self.tag_set]]
