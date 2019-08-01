# import requests
from coinapi_v1 import CoinAPIv1
import datetime
import SQLAlchemy
import numpy as np

test_key = 'E2B37F93-9B44-4E58-8E38-1F9B6A31A8D0'


conn_string = "port=5432 dbname=crypto user=postgres password=password"
conn=psycopg2.connect(conn_string)
api = CoinAPIv1(test_key)
db = sqlalchemy.create_engine(conn_string)
engine = db.connect()

def get_year_of_data():
    crypto_symbol = input("Enter a crypto symbol (BTC, ETH, XRP, DOGE): ")
    symbols = api.metadata_list_symbols()
    if crypto_symbol not in symbols:
        print("Please select a symbol from this list: ")
        print(symbols)
        get_year_of_data()
    else:
        datetime = datetime.datetime.today()
        start_time = datetime.date(datetime.year-1, datetime.month, datetime.day).isoformat()
        # For the purpose of thos excercise we are using USD as a pricing currency. This could
        # also be made customizable.
        asset_id_quote = 'USD'
        asset_id_base = crypto_symbol
        exchange_id = 'BITSTAMP'
        symbol_type = f'{exchange_id}_SPOT_{asset_id_base}_{asset_id_quote}'
        ohlcv_historical = api.ohlcv_historical_data(symbol_type, {'period_id': '1MIN', 'time_start': start_time})
        ohlcv_historical['asset_id_base'] = ohlcv_historical
        data = pd.read_json(ohlcv_historical, orient='records', dtype={
            'time_close': np.datetime64,
            'time_open': np.datetime64,
            'time_period_end': np.datetime64,
            'time_period_start': np.datetime64,
            "time_period_start": np.datetime64,
            "time_period_end": np.datetime64,
            "time_open": np.datetime64,
            "time_close": np.datetime64,
            "price_open": np.float64,
            "price_high": np.float64,
            "price_low": np.float64,
            "price_close": np.float64,
            "volume_traded": np.float64,
            "trades_count": np.int64
        })
        data.to_sql(name='crypto', con=engine, if_exists = 'replace', index=False)
