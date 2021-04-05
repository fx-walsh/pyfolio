import pandas as pd
from sqlalchemy import create_engine
import datetime

def monthly_summary(x):
    d = {}
    d['lowest_close'] = x['close_price'].min()
    d['highest_close'] = x['close_price'].max()
    d['avg_close'] = x['close_price'].mean()
    d['lowest_open'] = x['open_price'].min()
    d['highest_open'] = x['open_price'].max()
    d['avg_open'] = x['open_price'].mean()
    d['highest_high'] = x['high_price'].max()
    d['lowest_low'] = x['low_price'].min()
    d['daily_return_volatility'] = x['daily_return'].std()
    d['avg_daily_return'] = x['daily_return'].mean()
    d['monthly_return'] = (x['daily_return'] + 1).prod()
    d['total_price_change'] = x['daily_price_change'].sum()
    d['daily_volume_volatility'] = x['volume_perc_change'].std()
    d['avg_volume_change'] = x['volume_perc_change'].mean()
    d['monthly_perc_volume_change'] = (x['volume_perc_change'] + 1).prod()
    d['total_volume_change'] = x['volume_perc_change'].sum()
    
    return pd.Series(d, index=['lowest_close', 'highest_close', 'avg_close', 'lowest_open', 'highest_open','avg_open',
                              'highest_high', 'lowest_low', 'daily_return_volatility', 'avg_daily_return', 
                               'monthly_return','total_price_change', 'daily_volume_volatility', 'avg_volume_change', 
                               'monthly_perc_volume_change','total_volume_change'])


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

def create_min_max_date(current_date):

    max_year = current_date.year
    min_year = current_date.year if current_date.month != 1 else current_date.year - 1

    max_month = current_date.month
    min_month = current_date.month - 1 if current_date.month != 1 else 12

    max_day = 1
    min_day = 1

    max_date = datetime.date(max_year, max_month, max_day)
    min_date = datetime.date(min_year, min_month, min_day)

    max_date = max_date - datetime.timedelta(days=1)

    return [min_date, max_date]
