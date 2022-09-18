import csv
import request_data as rd
import clean_data as cd 
import XGBoost as xg 
import NN as n
import pandas as pd

class TA_predict:

    def __init__(self, data_collection, predic, train_model, csv_file, clean_data_name, model_name, model_type, load_model):
        self.data_collection = data_collection
        self.predic = predic
        self.train_model = train_model
        self.csv_file = csv_file
        self.clean_data_name1 = f'{model_name}_clean_data.h5'
        self.clean_data_name = clean_data_name
        self.model_name = model_name
        self.model_type = model_type
        self.load_name = load_model


        if self.data_collection and self.predic:
            inst = rd.Obtain_Data(self.csv_file, self.model_name, True)
            inst.ticker_list()
        elif (self.data_collection) and (self.predic == False):
            inst = rd.Obtain_Data(self.csv_file, self.model_name, False)
            inst.ticker_list()

        if self.data_collection:
            xgb = xg.XGboost(self.csv_file, self.clean_data_name1, self.predic, self.model_name)
        else:
            xgb = xg.XGboost(self.csv_file, self.clean_data_name, self.predic, self.model_name)

        if self.train_model == True:
            xgb.train_model(2,'binary')
            xgb.predict_model_new('binary')
            xgb.train_model(6,'multi')
            xgb.predict_model_new('multi')
        else:
            if self.model_type == 'binary':
                xgb.load_model(f'{self.load_name}_binary.model')
                xgb.predict_model_pred('binary')
            elif self.model_type == 'multi':
                xgb.load_model(f'{self.load_name}_multi.model')
                xgb.predict_model_pred('multi')
            elif self.model_type == 'both':
                xgb.load_model(f'{self.load_name}_binary.model')
                xgb.predict_model_pred('binary')
                xgb.load_model(f'{self.load_name}_multi.model')
                xgb.predict_model_pred('multi')
   
    

    '''
    nn = n.NeuralNetwork('SP500.csv','SP500_full_data.h5')
    nn.collect_data()
    nn.train_NN()
    '''