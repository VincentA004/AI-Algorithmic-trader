import pandas as pd 

class clean_data:

    def __init__(self, type1):
        self.type = type1

    
    def clean_data(self, ticker_d, ticker):
        ticker_data = ticker_d
        try:
            ticker_data['Returns_Binary'] = self.calc_returns(ticker_data['Close'])
            ticker_data['Returns_Multi'] = self.calc_returns_multi(ticker_data['Close'])
            ticker_data = ticker_data.dropna()

            ticker_data['Close'] = ticker_data['Close'].astype(float)
            ticker_data['Volume'] = ticker_data['Volume'].astype(float)

            ticker_data['TEMA5'] = ticker_data['TEMA5']/ticker_data['Close']
            ticker_data['TEMA10'] = ticker_data['TEMA10']/ticker_data['Close']
            ticker_data['TEMA20'] = ticker_data['TEMA20']/ticker_data['Close']
            ticker_data['TEMA50'] = ticker_data['TEMA50']/ticker_data['Close']
            ticker_data['TEMA100'] = ticker_data['TEMA100']/ticker_data['Close']

            ticker_data['SMA5'] = ticker_data['SMA5']/ticker_data['Close']
            ticker_data['SMA10'] = ticker_data['SMA10']/ticker_data['Close']
            ticker_data['SMA50'] = ticker_data['SMA50']/ticker_data['Close']
            ticker_data['SMA100'] = ticker_data['SMA100']/ticker_data['Close']
            ticker_data['SMA200'] = ticker_data['SMA200']/ticker_data['Close']

            ticker_data['OBV'] = ticker_data['OBV']/ticker_data['Volume']

            ticker_data = ticker_data.drop(columns = ['Open','Low','High','Close','Volume','Adjusted Close', 'Dividend Amount'])

            return ticker_data

        except:
            print(f'The stock {ticker} was not able to be cleaned.')

    def clean_data_wout(self, ticker_d, ticker):
        ticker_data = ticker_d
        try:
            ticker_data = ticker_data.dropna()

            ticker_data['Close'] = ticker_data['Close'].astype(float)
            ticker_data['Volume'] = ticker_data['Volume'].astype(float)

            ticker_data['TEMA5'] = ticker_data['TEMA5']/ticker_data['Close']
            ticker_data['TEMA10'] = ticker_data['TEMA10']/ticker_data['Close']
            ticker_data['TEMA20'] = ticker_data['TEMA20']/ticker_data['Close']
            ticker_data['TEMA50'] = ticker_data['TEMA50']/ticker_data['Close']
            ticker_data['TEMA100'] = ticker_data['TEMA100']/ticker_data['Close']

            ticker_data['SMA5'] = ticker_data['SMA5']/ticker_data['Close']
            ticker_data['SMA10'] = ticker_data['SMA10']/ticker_data['Close']
            ticker_data['SMA50'] = ticker_data['SMA50']/ticker_data['Close']
            ticker_data['SMA100'] = ticker_data['SMA100']/ticker_data['Close']
            ticker_data['SMA200'] = ticker_data['SMA200']/ticker_data['Close']

            ticker_data['OBV'] = ticker_data['OBV']/ticker_data['Volume']

            ticker_data = ticker_data.drop(columns = ['Open','Low','High','Close','Volume','Adjusted Close', 'Dividend Amount'])

            return ticker_data

        except:
            print(f'The stock {ticker} was not able to be cleaned.')

    def calc_returns(self, stock_df):
        dates = list(stock_df.index)

        label_dict = {}

        for count in range(len(dates)):
            try:
                ret = (float(stock_df.loc[dates[count+5]]) / float(stock_df.loc[dates[count]]))
                if ret <= 1:
                    label_dict[dates[count]] = 0
                else:
                    label_dict[dates[count]] = 1
                
            except:
                label_dict[dates[count]] = None
        
        return pd.Series(label_dict)
    
    def calc_returns_multi(self, stock_df):
        dates = list(stock_df.index)

        label_dict = {}

        for count in range(len(dates)):
            try:
                ret = (float(stock_df.loc[dates[count+5]]) / float(stock_df.loc[dates[count]]))
                if ret <= .90:
                    label_dict[dates[count]] = 0
                elif ret <= .95:
                    label_dict[dates[count]] = 1
                elif ret <= 1.0:
                    label_dict[dates[count]] = 2
                elif ret <= 1.05:
                    label_dict[dates[count]] = 3
                elif ret <= 1.10:
                    label_dict[dates[count]] = 4
                elif ret > 1.10:
                    label_dict[dates[count]] = 5
                
            except:
                label_dict[dates[count]] = None
        
        return pd.Series(label_dict)
          
            
                
            
        
        

