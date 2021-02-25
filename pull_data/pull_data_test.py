import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io
import string
import requests
from bs4 import BeautifulSoup


print("it's working")

start = datetime.datetime(2000,1,1)
end = datetime.datetime(2021,2,1)

print("Start Date: ", start)
print("End Date: ", end)

#==========================================================
# Pulling all of the tickers
#==========================================================

# website url where tickers exits
def scrape_tickers(
    exchange: str = 'NYSE',
    url: str = 'eoddata.com/stocklist',
    letter: str = 'A',
    csv_writer = None
):

    full_url = f'http://{url}/{exchange}/{letter}.htm'
    page = requests.get(full_url) 
    soup = BeautifulSoup(page.content, 'html.parser')

    quotes_table = soup.find_all('table', class_='quotes')[0]
    quotes_rows = quotes_table.find_all('tr')

    for i, row in enumerate(quotes_rows):
        if i != 0:
            row_elements = row.find_all('td')

            ticker = row_elements[0].find('a').get_text()
            ticker_title = row_elements[1].get_text()

            data_row = [exchange, ticker, ticker_title]

            data_row_string = ','.join(data_row)

            csv_writer.write(data_row_string)
            csv_writer.write("\n")
            


all_letters = list(string.ascii_uppercase)

today = datetime.date.today()

file_name = f'C:/Users/francisw/Desktop/repos/data/tickers_{today}.csv'

csv_file = open(file_name, 'w')
csv_file.write('EXCHANGE,TICKER,TICKER_TITLE')
csv_file.write("\n")

# NYSE tickers
for letter in all_letters:

    scrape_tickers(letter=letter, exchange='NYSE', csv_writer=csv_file)


# NASDAQ tickers
for letter in all_letters:

    scrape_tickers(letter=letter, exchange='NASDAQ', csv_writer=csv_file)

csv_file.close()
