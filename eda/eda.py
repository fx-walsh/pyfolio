import pandas as pd
import yfinance as yf
import datetime
import time
import requests
from pandas_datareader import data as pdr

msft = yf.Ticker("MSFT")

start = datetime.datetime(2000,1,1)
end = datetime.datetime(2021,2,1)

print("Start Date: ", start)
print("End Date: ", end)

x = msft.history(interval='1mo', start=start, end=end)

print(x)
print(x.columns)