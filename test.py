import pandas as pd 

data = pd.HDFStore('SP500_clean_data.h5')

print(data.keys())