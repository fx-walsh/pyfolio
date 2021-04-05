import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io
import string
import requests
from bs4 import BeautifulSoup
from sqlalchemy import text
from etl_helpers import monthly_summary
import keyring
import numpy as np

def pull_historical_data(start_date, end_date, engine):
    
    with engine.connect() as conn:
    
        conn.execute(text('TRUNCATE TABLE lkp.ticker_info'))

        ticker_q = text('SELECT t.* FROM lkp.ticker as t LEFT JOIN lkp.delisted as d on t.ticker = d.ticker WHERE d.ticker is NULL')
        tickers_df = pd.read_sql(
            ticker_q,
            con=conn
        )

        current_year_month = str(start_date)
        current_year_month = current_year_month[:7]

        monthly_sum_tickers_q = (
            'SELECT distinct ticker FROM raw.monthly_summary GROUP BY ticker HAVING '
            f"max(year_month) >= '{current_year_month}'"
        )
        monthly_sum_tickers_q = text(monthly_sum_tickers_q)
        monthly_sum_tickers = pd.read_sql(
            monthly_sum_tickers_q,
            con=conn
        )
    
        div_tickers_q = (
            'SELECT distinct ticker, max(market_date) as max_market_date FROM raw.actions GROUP BY ticker'
        )
        div_tickers_q = text(div_tickers_q)
        div_tickers = pd.read_sql(
            div_tickers_q,
            con=conn
        )
    
        all_tickers = tickers_df.ticker.tolist()
        monthly_summary_al = monthly_sum_tickers.ticker.tolist()
        
        for ticker in all_tickers:
            print("------------------------------------------------------------------")
            print("Pulling Data for Ticker: ", ticker)

            ticker_yf = yf.Ticker(ticker)

            if ticker not in monthly_summary_al:

                print('1. Pulling monthly stock prices')

                ticker_data = ticker_yf.history(interval='1d', start=start_date, end=end_date)

                if ticker_data.empty:
                    print("Ticker data does not exist")
                    ticker_dict = {'ticker': ticker}

                    temp_ticker_df = pd.DataFrame(ticker_dict, index=[0])

                    try:
                        temp_ticker_df.to_sql(
                            name='delisted',
                            schema='lkp',
                            con=conn,
                            if_exists='append',
                            index=False
                        )
                    except:
                        print('Ticker already exists in delisted df: ', ticker)
                        ticker_background = {}
                else:
                    # loading historical stock price info
                    ticker_data['ticker'] = ticker
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
            else:
                print('1. Already loaded monthly stock prices')


            print('2. pulling historical dividends and stock splits')
            # loading historical actions data
            
            max_div_ticker_date_ser = div_tickers.max_market_date[div_tickers.ticker == ticker]

            if not max_div_ticker_date_ser.empty:
                max_div_ticker_date = pd.to_datetime(max(max_div_ticker_date_ser))
            else:
                max_div_ticker_date = None

            ticker_actions = ticker_yf.actions
            ticker_actions.reset_index(inplace=True)
            ticker_actions.columns = ['market_date', 'dividends', 'stock_splits']
            ticker_actions['ticker'] = ticker
            ticker_actions = ticker_actions[['ticker', 'market_date', 'dividends', 'stock_splits']]

            if max_div_ticker_date:

                ticker_actions = ticker_actions[ticker_actions.market_date > max_div_ticker_date]

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
                ticker_background = ticker_yf.info
            except:
                print('Info produces error for ticker: ', ticker)
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

            ticker_info_df['ticker'] = ticker

            ticker_info_df.to_sql(
                name='ticker_info',
                schema='lkp',
                con=conn,
                if_exists='append',
                index=False
            )


    