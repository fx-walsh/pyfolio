"""
engine = create_engine(
    "postgresql+pg8000://scott:tiger@localhost/test",
    execution_options={
        "isolation_level": "REPEATABLE READ"
    }
)
"""

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
"""
engine = create_postgres_engine(
    username='',
    password='',
    dialect_driver='postgresql',
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
    port='5432',
    database='folio'
)
"""

#print(engine)

#conn = engine.connect()


#print(conn)

#conn.execute('CREATE DATABASE FOLIO')



engine1 = create_postgres_engine(
    username='',
    password='',
    dialect_driver='postgresql',
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
    port='5432',
    database='folio'
)

#conn = engine1.connect()

#conn.execution_options(isolation_level="AUTOCOMMIT").execute('CREATE SCHEMA LKP')


meta = MetaData(engine1)
meta.reflect(bind=engine1)

#print(meta.tables)

ticker = Table(
    'ticker', meta,
    Column('exchange', String),
    Column('ticker', String, primary_key=True),
    Column('company_name', String),
    schema='lkp'
)
meta.create_all()





