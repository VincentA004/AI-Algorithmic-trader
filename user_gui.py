import stock_runner as sr

# Parameters in order
# Data_Collection: (True or False) Determines whether you want new data collected. If set to False, user provided data will be used.
# Predic: (True or False) If set to True, will provide csv file with predictions about stocks. Set to False if you are training a new model.
# Train_Model: (True or False) Set to True if you want to train model with new data or want updated model parameters,
# CSV_File: Provide CSV file with ticker symbols of stocks that you want to analyze. The name of the CSV file of the csv file must be provided in quotes. Ex: 'SP500.csv'
# Clean_Data_Name: If Data_Collection is set to False, provide name of file that contains the clean data. If Data_collection is set to True, these will be the name of the saved data file.
# Model_Name: This will be the name associated with saved files regarding this run.
# Model_Type: ('binary', 'multi', 'both') 



#runner = sr.TA_predict(False, True, False,'2020-12-22-watchlist.csv','2020-12-22-watchlist_clean_data.h5','2020-12-22-watchlist', 'both', 'SP500')

runner = sr.TA_predict(True, False, True,'SP500.csv','SP500_clean_data.h5','SP500', 'both', 'SP500')