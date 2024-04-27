import pickle

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


io_path = f'../Data Analysis- Are F2P Games the Solomn Future/list_of_games_data.pkl'
with open(io_path, 'rb') as f:
        list_of_games = pickle.load(f)

list_of_games