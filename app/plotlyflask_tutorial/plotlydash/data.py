"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd
from utils import create_postgres_engine
import keyring
import config as conf
from datetime import date
import datetime


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

def create_dataframe(ticker_list, min_date, max_date):
    """Create Pandas DataFrame from local CSV.""" 
    ticker_list_clean = [ticker.upper() for ticker in ticker_list]

    if len(ticker_list_clean) > 1:
        ticker_list_str = "', '".join(ticker_list_clean)
    else:
        ticker_list_str = ticker_list_clean[0]
    
    ticker_list_str = f"('{ticker_list_str}')"

    min_date = str(min_date)
    max_date = str(max_date)

    min_date = min_date[:7]
    max_date = max_date[:7]

    query = (
        "SELECT * FROM raw.monthly_summary "
        f"WHERE ticker in {ticker_list_str} "
        f"and year_month >= '{min_date}' and year_month <= '{max_date}'"
        " order by ticker, year_month"
    )

    username = conf.Config.DB_USERNAME

    engine = create_postgres_engine(
        username=username,
        password=keyring.get_password('folio', username),
        dialect_driver='postgresql',
        host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
        port='5432',
        database='folio'
    )

    with engine.connect() as conn:
        #res = conn.execute(text(query))
        #data = res.fetchall()

        data = pd.read_sql(
            con=conn,
            sql=query
        )
    
    return data

def pull_tickers():

    query = f"SELECT distinct ticker FROM lkp.ticker_info order by ticker"

    username = conf.Config.DB_USERNAME

    engine = create_postgres_engine(
        username=username,
        password=keyring.get_password('folio', username),
        dialect_driver='postgresql',
        host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
        port='5432',
        database='folio'
    )

    with engine.connect() as conn:
        #res = conn.execute(text(query))
        #data = res.fetchall()

        data = pd.read_sql(
            con=conn,
            sql=query
        )

        data_list = data.ticker.tolist()
    
    return data_list

def pull_tickers_update():

    query = f"select distinct ti.ticker, t.company_name from lkp.ticker_info as ti left join lkp.ticker as t on ti.ticker = t.ticker order by ti.ticker"

    username = conf.Config.DB_USERNAME

    engine = create_postgres_engine(
        username=username,
        password=keyring.get_password('folio', username),
        dialect_driver='postgresql',
        host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
        port='5432',
        database='folio'
    )

    with engine.connect() as conn:
        #res = conn.execute(text(query))
        #data = res.fetchall()

        data = pd.read_sql(
            con=conn,
            sql=query
        )

    values = data.ticker.tolist()

    data['label'] = data.ticker + ' : ' + data.company_name

    labels = data.label.tolist()

    return_dict = {
        'values': values,
        'labels': labels
    }

    return return_dict


def pull_dates():

    query = f"SELECT min(year_month) as min_year_month, max(year_month) as max_year_month FROM raw.monthly_summary"

    username = conf.Config.DB_USERNAME

    engine = create_postgres_engine(
        username=username,
        password=keyring.get_password('folio', username),
        dialect_driver='postgresql',
        host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
        port='5432',
        database='folio'
    )

    with engine.connect() as conn:
        #res = conn.execute(text(query))
        #data = res.fetchall()

        data = pd.read_sql(
            con=conn,
            sql=query
        )

        min_year_month = data.min_year_month[0]
        max_year_month = data.max_year_month[0]
        
        min_date = date(int(min_year_month[:4]), int(min_year_month[-2:]), 1)
        max_date_temp = date(int(max_year_month[:4]), int(max_year_month[-2:]), 1)

        max_date = last_day_of_month(max_date_temp)

    
    return [min_date, max_date]


def query_to_pandas(query):

    username = conf.Config.DB_USERNAME

    engine = create_postgres_engine(
        username=username,
        password=keyring.get_password('folio', username),
        dialect_driver='postgresql',
        host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
        port='5432',
        database='folio'
    )

    with engine.connect() as conn:
        #res = conn.execute(text(query))
        #data = res.fetchall()

        data = pd.read_sql(
            con=conn,
            sql=query
        )

 
    return data
    