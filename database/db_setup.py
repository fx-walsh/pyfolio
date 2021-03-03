from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer

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
    username='',
    password='',
    dialect_driver='postgresql',
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
    port='5432',
    database='folio'
)

with engine.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT").execute('CREATE DATABASE FOLIO')


engine1 = create_postgres_engine(
    username='',
    password='',
    dialect_driver='postgresql',
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
    port='5432',
    database='folio'
)

with engine1.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT").execute('CREATE SCHEMA LKP')
