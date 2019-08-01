# import requests
from coinapi_v1 import CoinAPIv1
import datetime
import sqlalchemy
import numpy as np
import psycopg2
import pandas as pd

test_key = 'E2B37F93-9B44-4E58-8E38-1F9B6A31A8D0'


api = CoinAPIv1(test_key)
db = sqlalchemy.create_engine('postgresql://postgres:password@localhost/crypto')
engine = db.connect()

def get_year_of_data():
    crypto_symbol = input("Enter a crypto symbol (BTC, ETH, XRP, DOGE): ")
    # symbols = api.metadata_list_symbols()
    symbols = ["BTC", "ETH", "XRP", "DOGE"]
    if crypto_symbol not in symbols:
        print("Please select a symbol from this list: ")
        get_year_of_data()
    else:
        today = datetime.datetime.today()
        start_time = datetime.date(today.year-1, today.month, today.day).isoformat()
        # For the purpose of those excercise we are using USD as a pricing currency. This could
        # also be made customizable.
        asset_id_quote = 'USD'
        # asset_id_quote = input("Currency: ")
        asset_id_base = crypto_symbol
        exchange_id = 'BITSTAMP'
        symbol_type = f'{exchange_id}_SPOT_{asset_id_base}_{asset_id_quote}'
        ohlcv_historical = api.ohlcv_historical_data(symbol_type, {'period_id': '1MIN', 'time_start': start_time})
        # ohlcv_historical['asset_id_base'] = ohlcv_historical
        data = pd.DataFrame(ohlcv_historical)
        data.to_sql(name='crypto', con=engine, if_exists = 'replace', index=False)
get_year_of_data()




    
