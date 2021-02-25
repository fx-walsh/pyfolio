import pandas as pd
import yfinance as yf
import datetime
import time
import requests
from pandas_datareader import data as pdr

msft = yf.Ticker("MSFT")

print(msft.history(period='max'))
