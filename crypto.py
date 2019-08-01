# import requests
from coinapi_v1 import CoinAPIv1
import datetime
import sqlalchemy
import numpy as np
import psycopg2
import pandas as pd
from matplotlib import pyplot
from sklearn.ensemble import RandomForestRegressor
from pylab import rcParams

test_key = 'E2B37F93-9B44-4E58-8E38-1F9B6A31A8D0'


api = CoinAPIv1(test_key)
db = sqlalchemy.create_engine('postgresql://jmooney@localhost/crypto')
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


def read_data():
    query = "SELECT * FROM crypto"
    df = pd.read_sql(query, engine)
    #Remove UTC timezone information
    df['time_open'] = pd.to_datetime(df['time_open']).dt.tz_localize(None)
    df['time_close'] = pd.to_datetime(df['time_close']).dt.tz_localize(None)
    df['time_period_start'] = pd.to_datetime(df['time_period_start']).dt.tz_localize(None)
    df['time_period_end'] = pd.to_datetime(df['time_period_end']).dt.tz_localize(None)
    #Convert timestampts to numeric values (seconds since epoch time)
    df['time_open_epoch'] = (df['time_open'] - datetime.datetime(1970,1,1)).dt.total_seconds()
    df['time_close_epoch'] = (df['time_close'] - datetime.datetime(1970,1,1)).dt.total_seconds()
    df['time_period_start_epoch'] = (df['time_period_start'] - datetime.datetime(1970,1,1)).dt.total_seconds()
    df['time_period_end_epoch'] = (df['time_period_end'] - datetime.datetime(1970,1,1)).dt.total_seconds()
    print(df.columns)
    return df

df = read_data()

def plot_data(df):
    df.plot(kind='scatter', x='time_open_epoch', y='price_open')
    pyplot.show()

def select_features(df):
    inputs = df[['volume_traded', 'trades_count', 'time_open_epoch', 'time_close_epoch']]
    X = inputs.values
    Y = df['price_high'].values
    model = RandomForestRegressor(n_estimators=50, random_state=1, min_samples_split=4)
    model.fit(X,Y)
    print(model.feature_importances_)
    names = inputs.columns.values[0:-1]
    count = [i for i in range(len(names))]
    # pyplot.bar(count, model.feature_importances_)
    # pyplot.xticks(count, names)
    # pyplot.show()

select_features(df)
plot_data(df)
