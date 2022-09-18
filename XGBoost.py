import pandas as pd 
import xgboost as xgb 
import csv
import math
import numpy as np
import logging 
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


class XGboost:
    def __init__(self, ticker_list, data_file, predic, name):
        self.csv_list = ticker_list
        self.cleandf = pd.HDFStore(data_file)
        self.name = name
        self.predic = predic

        self.model = xgb.Booster({'nthread': 4})

        logging.basicConfig(filename = f'hypertesting{self.name}.log', filemode= 'w', level = logging.INFO)

        if self.predic == True:
            self.x_predicdata = pd.DataFrame()
            self.pred_collect_data()
        else:
            self.X_train = pd.DataFrame()
            self.X_test = pd.DataFrame()
            self.Y_train_multi = pd.DataFrame()
            self.Y_test_multi = pd.DataFrame()
            self.Y_train_binary = pd.DataFrame()
            self.Y_test_binary = pd.DataFrame()
            self.collect_data()

        

    

    def collect_data(self):
        open_file = open(self.csv_list, 'r')
        csv_file = csv.reader(open_file, delimiter = ',')


        ticker_list = list(csv_file)

        for ticker in ticker_list:
            try:
                clean_data = self.cleandf.get(ticker[0])
                
                x_data = clean_data.iloc[:,:-2]
                binary = clean_data.iloc[:, -2:-1]
                multi = clean_data.iloc[:, -1:]
                
                split_num = self.get_splits(x_data)

                self.X_train = pd.concat([x_data.iloc[:split_num,:], self.X_train])
                self.X_test = pd.concat([x_data.iloc[split_num:,:], self.X_test])
                self.Y_train_binary = pd.concat([binary.iloc[:split_num,:], self.Y_train_binary])
                self.Y_test_binary = pd.concat([binary.iloc[split_num:,:], self.Y_test_binary])
                self.Y_train_multi = pd.concat([multi.iloc[:split_num,:], self.Y_train_multi])
                self.Y_test_multi = pd.concat([multi.iloc[split_num:,:], self.Y_test_multi])
                
            except:
                print(f"The stock {ticker} was not able to be incorporated.")
        
        self.D_train_binary = xgb.DMatrix(self.X_train, label = self.Y_train_binary)
        self.D_test_binary = xgb.DMatrix(self.X_test, label = self.Y_test_binary)
        self.D_train_multi = xgb.DMatrix(self.X_train, label = self.Y_train_multi)
        self.D_test_multi = xgb.DMatrix(self.X_test, label = self.Y_test_multi)


    def pred_collect_data(self):
        open_file = open(self.csv_list, 'r')
        csv_file = csv.reader(open_file, delimiter = ',')

        self.ticker_list = list(csv_file)

        for ticker in self.ticker_list.copy():
            try:
                clean_data = self.cleandf.get(ticker[0])
                self.x_predicdata = pd.concat([clean_data.iloc[-1:], self.x_predicdata])
               
            except:
                print(f"The stock {ticker} was not able to be incorporated.")
                self.list = self.ticker_list.remove(ticker)
        
        self.D = xgb.DMatrix(self.x_predicdata)


    def get_splits(self, data):
        split = math.floor(len(data)*.8)
        return split
    
    def train_model(self, num_class, return_type):

        param = {
            'gpu_id': 0,
            'gamma': 4,
            'tree_method': 'gpu_hist',
            'eta': .01,
            'max_depth': 1,
            'objective': 'multi:softprob',
            'num_class': num_class,
            'sampling_method': 'gradient_based',
            'subsample': .6}

        steps = 1000

        label = {}
        if return_type == 'binary':
            self.model = xgb.train(param, self.D_train_binary, steps)
        else:
            self.model = xgb.train(param, self.D_train_multi, steps)

        logging.info(param)
        logging.info(label)

        self.model.save_model(f'{self.name}_{return_type}.model')

    def load_model(self, model_name):
       
        self.model.load_model(model_name)

    def predict_model_new(self, return_type):

        if return_type == 'binary':
            preds = self.model.predict(self.D_test_binary)
            results = []
            for count, x in enumerate(preds):
                if x[1] > .55:
                    results.append(1)
                else:
                    results.append(0)
            actual = self.Y_test_binary.values.tolist()
            total_count = 0
            right_count = 0
            for x in range(len(actual)):
                if results[x] == 1:
                    total_count += 1
                    if actual[x][0] == 1:
                        right_count += 1
                
            print(f"Right Count: {right_count}")
            print(f"Total Count: {total_count}")
            print(right_count/total_count)
            best_preds = np.asarray([np.argmax(line) for line in preds])
            logging.info("Precision = {}".format(precision_score(self.Y_test_binary, best_preds, average='macro')))
            logging.info("Recall = {}".format(recall_score(self.Y_test_binary,  best_preds, average='macro')))
            logging.info("Accuracy = {}\n".format(accuracy_score(self.Y_test_binary,  best_preds)))
        else:
            preds = self.model.predict(self.D_test_multi)
            print(preds)
            best_preds = np.asarray([np.argmax(line) for line in preds])
            logging.info("Precision = {}".format(precision_score(self.Y_test_multi, best_preds, average='macro')))
            logging.info("Recall = {}".format(recall_score(self.Y_test_multi, best_preds, average='macro')))
            logging.info("Accuracy = {}\n".format(accuracy_score(self.Y_test_multi, best_preds)))

    def predict_model_pred(self, return_type):

        preds = self.model.predict(self.D)
        best_preds = np.asarray([np.argmax(line) for line in preds])
        logging.info(preds)
        logging.info(best_preds)
        

        results = []
        preds_no = []
        preds_yes = []
        for x in enumerate(preds):
            preds_no.append(x[1][0])
            preds_yes.append(x[1][1])
    
            if x[1][1] > .50:
                results.append(1)
            else:
                results.append(0)
        
        self.x_predicdata['Ticker Symbol'] = pd.DataFrame(self.ticker_list, index = self.x_predicdata.index)
        self.x_predicdata["Predictions_Prob_No"] = pd.DataFrame(preds_no, index = self.x_predicdata.index)
        self.x_predicdata["Predictions_Prob_Yes"] = pd.DataFrame(preds_yes, index = self.x_predicdata.index)
        self.x_predicdata['Predicted Returns'] = pd.DataFrame(results, index = self.x_predicdata.index)
        self.x_predicdata.to_csv(f'{self.name}_predic_{return_type}.csv')

