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

engine = create_postgres_engine(
    username='postgres',
    password='Micail@2',
    dialect_driver='postgresql',
    host='localhost',
    port='1234',
    database='folio'
)

meta = MetaData(engine, schema='lkp')
meta.reflect(bind=engine)

#print(meta.tables)

ticker = meta.tables['lkp.ticker']

"""
ticker = Table(
    'ticker', meta,
    Column('exchange', String, primary_key=True),
    Column('ticker', String),
    Column('company_name', String),
    schema='lkp'
)
meta.create_all()
"""

ins = ticker.insert().values(
      exchange='NYSE',
      ticker='APPL',
      company_name='Apple')
conn = engine.connect()
conn.execute(ins)

