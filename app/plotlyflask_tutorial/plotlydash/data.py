"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd
from utils import create_postgres_engine
import keyring

def create_dataframe():
    """Create Pandas DataFrame from local CSV."""
    #df = pd.read_csv("data/311-calls.csv", parse_dates=["created"])
    #df["created"] = df["created"].dt.date
    #df.drop(columns=["incident_zip"], inplace=True)
    #num_complaints = df["complaint_type"].value_counts()
    #to_remove = num_complaints[num_complaints <= 30].index
    #df.replace(to_remove, np.nan, inplace=True)
    
    ticker_clean = 'msft'.upper()

    query = f"SELECT * FROM raw.monthly_prices WHERE ticker = '{ticker_clean}'"

    engine = create_postgres_engine(
        username='fwalsh',
        password=keyring.get_password('folio', 'fwalsh'),
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