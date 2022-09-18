import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd 
import csv
import math
import numpy as np
import logging 
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import clean_data as c

class NeuralNetwork:
    def __init__(self, ticker_list, full_data_file):
        self.csv_list = ticker_list
        self.fulldf = pd.HDFStore(full_data_file)
        self.cd = c.clean_data('type1')

        self.X_train = pd.DataFrame()
        self.X_test = pd.DataFrame()
        self.Y_train = pd.DataFrame()
        self.Y_test = pd.DataFrame()

        logging.basicConfig(filename = 'hypertesting.log', filemode= 'w', level = logging.INFO)

        self.collect_data()
        

    def collect_data(self):
        open_file = open(self.csv_list, 'r')
        csv_file = csv.reader(open_file, delimiter = ',')

        header_row = next(csv_file)

        ticker_list = list(csv_file)

        for ticker in ticker_list:
            try:
                full_data = self.fulldf.get(ticker[0])

                full_data['Returns'] = self.cd.calc_returns(full_data['Close'])

                full_data = full_data.dropna()

                x_data = full_data.iloc[:,:-1]
                y_data = full_data.iloc[:, -1:]
            

                x_data = x_data.drop(columns = ['Open','Low','High','Close','Volume','Adjusted Close', 'Dividend Amount'])

                norm_x_data = (x_data - x_data.min())/ (x_data.max() - x_data.min())

                split_num = self.get_splits(x_data)

                self.X_train = pd.concat([norm_x_data.iloc[:split_num,:], self.X_train])
                self.X_test = pd.concat([norm_x_data.iloc[split_num:,:], self.X_test])
                self.Y_train = pd.concat([y_data.iloc[:split_num,:], self.Y_train])
                self.Y_test = pd.concat([y_data.iloc[split_num:,:], self.Y_test])

            except:
                print(f"The stock {ticker} was not able to be incorporated.")

    def get_splits(self, data):
        split = math.floor(len(data)*.8)
        return split

    def train_NN_LTSM(self):
        self.model = keras.Sequential()
        self.model(layers.LSTM(128))
        self.model(layers.Dropout(.2))
        self.model(layers.LSTM(256))
        self.model(layers.Dropout(.5))
        self.model(layers.LSTM(128))
        self.model(layers.Dropout(.2))
        self.model(layers.LSTM(64))
        self.model(layers.LSTM(50))
        self.model(layers.Dense(2, activation = 'sigmoid'))

        self.model.compile(
            optimizer=keras.optimizers.RMSprop(),  
            
            loss=keras.losses.SparseCategoricalCrossentropy(),
            
            metrics=[keras.metrics.SparseCategoricalAccuracy()],
            )

        self.model.fit(self.X_train, self.Y_train, batch_size= 32, epochs = 20)

        print("Evaluate on test data")
        results = self.model.evaluate(self.X_test, self.Y_test, batch_size=128)
        print("test loss, test acc:", results)


    def train_NN(self):

        self.model = keras.Sequential(
            [layers.Dense(128, activation="relu"),
            layers.Dense(256, activation="relu"),
            layers.Dense(528, activation='relu'),
            layers.Dense(256, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(50, activation='relu'),
            layers.Dense(2, activation='sigmoid')])

        self.model.compile(
            optimizer=keras.optimizers.RMSprop(),  
            
            loss=keras.losses.SparseCategoricalCrossentropy(),
            
            metrics=[keras.metrics.SparseCategoricalAccuracy()],
            )

        self.model.fit(self.X_train, self.Y_train, batch_size= 32, epochs = 1)

        print("Evaluate on test data")
        results = self.model.evaluate(self.X_test, self.Y_test, batch_size=128)
        print("test loss, test acc:", results)


