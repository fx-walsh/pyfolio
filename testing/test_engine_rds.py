# required modules
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer
import pandas as pd

# function to make future engine creations a bit easier
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

# actually creating the engine to connect to the RDS database
engine1 = create_postgres_engine(
    username='fwalsh',
    password='Gotarheels!',
    dialect_driver='postgresql', # since we are using postgresql
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com', # in AWS terms this is your Endpoint
    port='5432', # you can also find this in your AWS dashboard if you forget
    database='folio' # this is the database within the engine that you want to connect to
)

# you need to run engine1.connect() in order to actually form a connection with your database
# it's recommended to use a context manager so that you will disconnect from the database 
# automicallly
with engine1.connect() as conn:
    # using pandas read_sql function to import a sql query directly to a pandas dataframe
    df = pd.read_sql(
        con=conn,
        sql=text('SELECT * FROM raw.monthly_summary FETCH FIRST 100 ROWS ONLY')
    )

    # you can also go the opposite direction i.e., from pandas df to sql table
    df.to_sql(
        name='first100_monthly_summary',
        con=conn,
        schema='raw',
        if_exists='replace' # other options here are to 'append' to existing table or have process 'fail'
    )

    # lastly in this example, you can also run sql directly like the following
    conn.execute('TRUNCATE TABLE raw.first100_monthly_summary')









