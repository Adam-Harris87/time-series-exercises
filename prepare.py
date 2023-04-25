import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

import acquire
from env import user, password, host
import os
# from acquire import wrangle_store_data

import warnings
warnings.filterwarnings("ignore")

# plotting defaults
plt.rc('figure', figsize=(13, 7))
plt.style.use('seaborn-whitegrid')
plt.rc('font', size=16)


def get_db_url(database):
    return f'mysql+pymysql://{user}:{password}@{host}/{database}'

def get_store_data():
    '''
    Returns a dataframe of all store data in the tsa_item_demand 
    database and saves a local copy as a csv file.
    '''
    query = '''
    SELECT *
    FROM items
    JOIN sales USING(item_id)
    JOIN stores USING(store_id) 
    '''
    
    df = pd.read_sql(query, get_db_url('tsa_item_demand'))
    
    df.to_csv('tsa_item_demand.csv', index=False)
    
    return df

def prep_sales_data(df):
    df['sale_date'] = pd.to_datetime(df.sale_date)
    df = df.set_index('sale_date').sort_index()
    return df

def create_new_columns(df):
    df['month'] = df.index.month_name()
    df['day_of_week'] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price
    return df

def wrangle_store_data():
    filename = 'tsa_item_demand.csv'
    
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        df = get_store_data()
        
    df = prep_sales_data(df)
    df = create_new_columns(df)
    
    return df

def get_plot_sales_amount_and_prices(df):
    df.groupby('sale_date').sale_amount.sum().plot()
    plt.title('Sales at every store over time')
    plt.show()
    
    df.groupby('item_id').item_price.mean().plot()
    plt.title('Price for each item')
    plt.show()

def prep_germany(df):
    '''
    This function will lowercase all column names, convert the date column to datetime
    set date as the index, create new columns for month and year, 
    the fill nulls with 0
    
    returns prepped DataFrame
    '''
    # set column names to lowercase
    df.columns = df.columns.str.lower().to_list()
    # convert date to datetime and set as index
    df.date = pd.to_datetime(df.date)
    df = df.set_index(df.date).sort_index().drop(columns='date')
    # create new columns for month and year
    df['month'] = df.index.month_name()
    df['year'] = df.index.year
    # fill null values with 0
    df = df.fillna(0)
    # return prepped dataFrame
    return df

def plot_distributions(df):
    '''
    This function will plot distributions of all columns in the dataframe
    '''
    not_object = df.columns[df.dtypes != 'O'].to_list()
    for col in not_object:
        df[col].plot()
        plt.title(f'Distribution of {col}')
        plt.show()

def wrangle_germany():
    '''
    this will acquire and prepare the germany dataset
    '''
    germany = prep_germany(acquire.get_germany())
    return germany

def split_time_data(df):
    '''
    This function will split a time series dataset into train and test sets,
    and return the split dataframes
    '''
    # get the index value at 80%
    split_index = round(len(df) * .8)
    # train will be 80% of the length of the original df, test will be the remaining
    train = df.iloc[:split_index]
    test = df.iloc[split_index:]
    # return the split dfs
    return train, test