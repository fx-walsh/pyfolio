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
from .global_vars import DB_USER, DB_PASSWORD



print("it's working")

start = datetime.datetime(2000,1,1)
end = datetime.datetime(2021,2,1)

print("Start Date: ", start)
print("End Date: ", end)

#==========================================================
# Pulling all of the tickers
#==========================================================

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

# website url where tickers exits
def scrape_tickers(
    table: Table,
    engine: sa.engine,
    exchange: str = 'NYSE',
    url: str = 'eoddata.com/stocklist',
    letter: str = 'A'
):

    full_url = f'http://{url}/{exchange}/{letter}.htm'
    page = requests.get(full_url) 
    soup = BeautifulSoup(page.content, 'html.parser')

    quotes_table = soup.find_all('table', class_='quotes')[0]
    quotes_rows = quotes_table.find_all('tr')

    with engine.connect() as conn:
        for i, row in enumerate(quotes_rows):
            if i != 0:
                row_elements = row.find_all('td')

                ticker = row_elements[0].find('a').get_text()
                ticker_title = row_elements[1].get_text()

                data_row = [exchange, ticker, ticker_title]

                ins = table.insert().values(
                    exchange=exchange,
                    ticker=ticker,
                    company_name=ticker_title
                )

                conn.execute(ins)

                #data_row_string = ','.join(data_row)

                #csv_writer.write(data_row_string)
                #csv_writer.write("\n")
            


engine = create_postgres_engine(
    username=DB_USER,
    password=DB_PASSWORD,
    dialect_driver='postgresql',
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
    port='5432',
    database='folio'
)


meta = MetaData(engine)
meta.reflect(bind=engine)

#print(meta.tables)

ticker = Table(
    'ticker', meta,
    Column('exchange', String, primary_key=True),
    Column('ticker', String),
    Column('company_name', String),
    schema='lkp'
)
meta.create_all()

today = datetime.date.today()

all_letters = list(string.ascii_uppercase)

# NYSE tickers
for letter in all_letters:

    scrape_tickers(
        table=ticker,
        engine=engine,
        letter=letter,
        exchange='NYSE'
    )

    scrape_tickers(
        table=ticker,
        engine=engine,
        letter=letter,
        exchange='NASDAQ'
    )


