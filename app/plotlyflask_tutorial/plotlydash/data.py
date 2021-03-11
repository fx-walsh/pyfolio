"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd
from utils import create_postgres_engine
import keyring
import config as conf

def create_dataframe(ticker_list):
    """Create Pandas DataFrame from local CSV."""
    #df = pd.read_csv("data/311-calls.csv", parse_dates=["created"])
    #df["created"] = df["created"].dt.date
    #df.drop(columns=["incident_zip"], inplace=True)
    #num_complaints = df["complaint_type"].value_counts()
    #to_remove = num_complaints[num_complaints <= 30].index
    #df.replace(to_remove, np.nan, inplace=True)
    
    ticker_list_clean = [ticker.upper() for ticker in ticker_list]

    if len(ticker_list_clean) > 1:
        ticker_list_str = "', '".join(ticker_list_clean)
    else:
        ticker_list_str = ticker_list_clean[0]
    
    ticker_list_str = f"('{ticker_list_str}')"

    query = f"SELECT * FROM raw.monthly_summary WHERE ticker in {ticker_list_str} order by ticker, year_month"

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
    