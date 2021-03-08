import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io
import string
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer
import sqlalchemy as sa
from utils import monthly_summary
import keyring
import numpy as np
#from .global_variables import DB_USER, DB_PASSWORD

print("it's working")

start = datetime.datetime(2000,1,1)
end = datetime.datetime(2021,2,28)

print("Start Date: ", start)
print("End Date: ", end)

def create_postgres_engine(
    username: str,
    password: str,
    dialect_driver: str,
    host: str,
    port: str,
    database: str
):
    db_url = f'{dialect_driver}://{username}:{password}@{host}:{port}/{database}'
    
    ret_eng = create_engine(db_url)

    return ret_eng


engine = create_postgres_engine(
    username='fwalsh',
    password=keyring.get_password('folio', 'fwalsh'),
    dialect_driver='postgresql',
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
    port='5432',
    database='folio'
)

with engine.connect() as conn:

    res = conn.execute(text('SELECT * FROM lkp.ticker'))
    tickers_info = res.fetchall()

    monthly_tickers_q = text('SELECT distinct ticker FROM raw.monthly_summary')
    monthly_tickers = pd.read_sql(
        monthly_tickers_q,
        con=conn
    )

    tickers_already_loaded = monthly_tickers.ticker.tolist()

    
    for ticker_info in tickers_info:
        
        if ticker_info[1] not in tickers_already_loaded:
            print("------------------------------------------------------------------")
            print("Pulling Data for Ticker: ", ticker_info[1])

            ticker = yf.Ticker(ticker_info[1])

            print('1. Pulling historical stock prices')
            #ticker_data = ticker.history(interval='1mo', start=start, end=end)
            ticker_data = ticker.history(interval='1d', start=start, end=end)

            if ticker_data.empty:
                print("Ticker data does not exist")
            else:
                # loading historical stock price info
                ticker_data['ticker'] = ticker_info[1]
                ticker_data.index.name = 'market_date'
                ticker_data.reset_index(inplace=True)

                new_cols = ['market_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'dividends', 'stock_splits', 'ticker']

                ticker_data.columns = new_cols

                ticker_data['year_month'] = ticker_data.market_date.astype(str).str[:7]

                ticker_data['daily_price_change'] = ticker_data.close_price - ticker_data.close_price.shift(1)
                ticker_data['daily_return'] = ticker_data.close_price / np.where(ticker_data.close_price.shift(1) == 0, .01, ticker_data.close_price.shift(1)) - 1
                ticker_data['volume_change'] = ticker_data.volume - ticker_data.volume.shift(1)
                ticker_data['volume_perc_change'] = ticker_data.volume / np.where(ticker_data.volume.shift(1) == 0, .01, ticker_data.volume.shift(1)) - 1

                ticker_data_monthly = ticker_data.groupby(['ticker', 'year_month']).apply(monthly_summary)

                ticker_data_monthly.reset_index(inplace=True)

                ticker_data_monthly.to_sql(
                    name='monthly_summary',
                    schema='raw',
                    con=conn,
                    if_exists='append',
                    index=False
                )

                print('2. pulling historical dividends and stock splits')
                # loading historical actions data
                ticker_actions = ticker.actions
                ticker_actions.reset_index(inplace=True)
                ticker_actions.columns = ['market_date', 'dividends', 'stock_splits']
                ticker_actions['ticker'] = ticker_info[1]
                ticker_actions = ticker_actions[['ticker', 'market_date', 'dividends', 'stock_splits']]

                ticker_actions.to_sql(
                    name='actions',
                    schema='raw',
                    con=conn,
                    if_exists='append',
                    index=False
                )

                print("3. pulling company info")
                # loading ticker info
                try:
                    ticker_background = ticker.info
                except:
                    print('Info produces error for ticker: ', ticker_info[1])
                    ticker_background = {}

                desired_cols = ['sector', 'fullTimeEmployees', 'longBusinessSummary', 'city', 'state', 'country', 'website']

                temp_dict = {}

                ticker_back_keys = ticker_background.keys()
                for col in desired_cols:
                    if col in ticker_back_keys:
                        temp_dict[col] = ticker_background[col]
                    else:
                        temp_dict[col] = np.NaN

                ticker_info_df = pd.DataFrame(temp_dict, index=[0])

                ticker_info_df.columns = ['sector', 'num_fulltime_emps', 'long_biz_summary', 'city', 'state', 'country', 'website']

                ticker_info_df['ticker'] = ticker_info[1]

                ticker_info_df.to_sql(
                    name='ticker_info',
                    schema='lkp',
                    con=conn,
                    if_exists='append',
                    index=False
                )


    