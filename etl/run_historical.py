import datetime
import keyring

import pull_historical as ph
from etl_helpers import create_postgres_engine, create_min_max_date


db_engine = create_postgres_engine(
    username='fwalsh',
    password=keyring.get_password('folio', 'fwalsh'),
    dialect_driver='postgresql',
    host='folio1.cd5sapiffloo.us-east-2.rds.amazonaws.com',
    port='5432',
    database='folio'
)

current_date = datetime.datetime.today()

date_range = create_min_max_date(current_date=current_date)

start_date = date_range[0]
end_date = date_range[1]

ph.pull_historical_data(
    start_date=start_date,
    end_date=end_date,
    engine=db_engine
)

