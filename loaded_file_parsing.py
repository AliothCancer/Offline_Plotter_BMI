
import pandas as pd



# create a dataframe with the csv file
def get_columns(file_name):
    df = pd.read_csv(file_name)
    return df.columns

def get_data(file_name, column):
    df = pd.read_csv(file_name)

    data = df[column]
    #print(data)
    #print(type(data))
    return data.to_numpy()



