from plotlyflask_tutorial import init_app

app = init_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

"""
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer
import sqlalchemy as sa
from utils import create_postgres_engine
import keyring

from flask import Flask
from flask import render_template
import pandas as pd
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<ticker>')
def monthly_data(ticker):
    
    ticker_clean = ticker.upper()

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
    
    return render_template('template.html', data=data)


if __name__ == '__main__':
    app.run()

"""