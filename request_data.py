import requests
import pandas as pd 
import time
import calc_TA as t
import csv
import clean_data as c


BASE_URL = 'https://www.alphavantage.co/query?'
API_KEY = 'CVXYL4XHJEIGFCTC'

class Obtain_Data:

    def __init__(self, file, name, predic):
        self.csv_file = file
        self.ta = t.calc_TA_data('1')
        self.full_data_file = pd.HDFStore(f'{name}_full_data.h5')
        self.clean_data_file = pd.HDFStore(f'{name}_clean_data.h5')
        self.cd = c.clean_data('1')
        self.predic = predic

    
    def get_ticker_data(self, ticker):
        try:
            param = {'function' : 'TIME_SERIES_DAILY_ADJUSTED', 'symbol' : ticker , 'outputsize': 'full', 'datatype': 'json', 'apikey': API_KEY}
           
            r = requests.get(BASE_URL, params = param)
        
            response_dict = r.json()
            print(r)
            fin_data = response_dict["Time Series (Daily)"]

            time.sleep(2)

            return fin_data

        except:
            print(f"The following {ticker} was not found.")
      
    def store_ticker_data(self, fulldf, data, ticker, cleandf):

        app = pd.DataFrame(data).T.iloc[::-1]

        full_stock_data = self.ta.gen_ta(app)

        fulldf.put(f"{ticker}", full_stock_data, format = "table")

        if self.predic == False:
            clean_data = self.cd.clean_data(full_stock_data, ticker)
        else:
            clean_data = self.cd.clean_data_wout(full_stock_data, ticker)

        cleandf.put(f"{ticker}", clean_data, format = "table")

    
    
    def ticker_list(self):
        open_file = open(self.csv_file,'r')
        csv_file = csv.reader(open_file, delimiter = ',')

        #self.index_name = next(csv_file)[0]
        
        ticker_list = list(csv_file)

        for count, ticker in enumerate(ticker_list):
            try:
                ticker_data = self.get_ticker_data(ticker[0])
                self.store_ticker_data(self.full_data_file, ticker_data, ticker[0], self.clean_data_file)
                print(f"{count}. {ticker[0]} was added and cleaned.")
            except:
                print(f'The {ticker[0]} could not be added/cleaned to the file')


    
    



