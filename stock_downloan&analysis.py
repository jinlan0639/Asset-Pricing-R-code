# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 22:24:52 2024

@author: Jinlan
"""

#%%

import os
os.chdir(r'D:\KCL\python\0.python_practise')
os.getcwd()


#%% data preparation

import pandas as pd
import numpy  as np
import yfinance as yf
import time
import datetime
from collections import Counter


##down all NASDAQ ticker csv from website 
## "https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download"

nasdaq = pd.read_csv("nasdaq.csv")
nasdaq_list = nasdaq["Symbol"].to_list()
print(nasdaq_list,len(nasdaq_list))


## record the began download time
print(time.asctime())

## download the data
data_download = yf.download(nasdaq_list[:100],interval="1wk",start='2023-01-01',group_by='ticker')


## droplevel:drop multi-index; iloc[:-1,:] drop the newest data -----commonly some error
data_wash = data_download.loc[:,(slice(None),"Close")].droplevel(1,axis=1).iloc[:-1,:]

print(data_new.shape)

## calculate weekday to make sure if there is abnormal data
print(Counter([i.weekday() for i in data_new.index]))

## pick the abnormal stock
abnormal_stock_list = data_wash.loc[[i for i in data_wash.index if i.weekday()!=6 ]].dropna(how="all",axis=1).columns.to_list()


## keep the normal data，drop the abnormal data
data = data_wash.loc[:,[i for i in data_wash.columns if i not in  abnormal_stock_list]].dropna( how='all',axis=0).dropna( how='all',axis=1)



#==================================deposite & read data=============================================================#

## I/O: deposite data
filename = 'NASDAQ_DATA_20240116'
h5s = pd.HDFStore( filename + '.h5s', 'w')
h5s['data'] = pd.DataFrame(data)
h5s.close()


## read data
h5s = pd.HDFStore(filename + '.h5s', 'r')
temp = h5s['data']
h5s.close()


#%% FAMA FRENCH DATA

#http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

from pandas_datareader.famafrench import get_available_datasets

import pandas_datareader.data as web

#save datasets list
fama_french_dataset_list = get_available_datasets()

#print Length of datasets available
print(len(get_available_datasets()))

ds = web.DataReader("F-F_Research_Data_Factors_weekly", "famafrench")


ds = web.DataReader("F-F_Momentum_Factor_daily", "famafrench")

#added custom date range for full data extraction
# set dates as min and max data ranges of original data





