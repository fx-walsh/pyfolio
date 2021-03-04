# pyfolio

## setting up your conda environment

1. open up comment prompt
2. If you haven't created the environment run this:

`conda env create -f environment.yml`

3. Once conda environment is created run:

`conda activate folio`

## setting up flask environment

1. in the app directory create a file called `.env`
2. inside file add the following environment variables:

```
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=randomstringofcharacters
LESS_BIN=/usr/local/bin/lessc
ASSETS_DEBUG=False
LESS_RUN_IN_DEBUG=False
COMPRESSOR_DEBUG=True
DB_USER=<your username>
```