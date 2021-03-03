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
#from .global_variables import DB_USER, DB_PASSWORD

print("it's working")

start = datetime.datetime(2000,1,1)
end = datetime.datetime(2021,3,1)

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
    password='Gotarheels!',
    dialect_driver='postgresql',
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
    port='5432',
    database='folio'
)

with engine.connect() as conn:

    res = conn.execute(text('SELECT * FROM lkp.ticker'))
    tickers_info = res.fetchall()

    monthly_tickers_q = text('SELECT distinct ticker FROM raw.monthly_prices')
    monthly_tickers = pd.read_sql(
        monthly_tickers_q,
        con=conn
    )

    tickers_already_loaded = monthly_tickers.ticker.tolist()

    
    for ticker_info in tickers_info:
        
        if ticker_info[1] not in tickers_already_loaded:
            print("Pulling Data for Ticker: ", ticker_info[1])
            print("------------------------------------------------------------------")

            ticker = yf.Ticker(ticker_info[1])

            ticker_data = ticker.history(interval='1mo', start=start, end=end)

            if ticker_data.empty:
                print("Ticker data does not exist")
            else:
                ticker_data['ticker'] = ticker_info[1]
                ticker_data.index.name = 'market_date'
                ticker_data.reset_index(inplace=True)

                new_cols = ['market_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'dividends', 'stock_splits', 'ticker']

                ticker_data.columns = new_cols

                ticker_data.to_sql(
                    name='monthly_prices',
                    schema='raw',
                    con=conn,
                    if_exists='append',
                    index=False
                )

    