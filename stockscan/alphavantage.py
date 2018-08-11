import numpy as np
import json
import requests


def get_apikey(f):
    #reading apikey.json
    apikey = list(json.load(open(f,"r")).values())[-1]
    '''
    this code is for reading apikey.txt
    with open(f,'r') as ff:
        apikey= ff.read().strip()
    '''
    return apikey


def query_time_series_intraday(symbol, f_apikey, interval='1min',outputsize= 'compact',datatype='json'):
    apikey = get_apikey(f_apikey)
    request = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+symbol+'&interval='+interval+'&datatype='+datatype+'&outputsize='+outputsize+'&apikey='+apikey
    items = requests.get(request).json()
    return items


def query_time_series_daily(symbol, f_apikey, outputsize= 'compact',datatype='json'):
    apikey = get_apikey(f_apikey)
    request = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&datatype='+datatype+'&outputsize='+outputsize+'&apikey='+apikey
    items = requests.get(request).json()
    return items


def get_historical_prices(symbol, end_date, start_date, apikey_filename):
    qout = query_time_series_daily(symbol, apikey_filename)
    stocks = qout["Time Series (Daily)"]
    dates = list(stocks.keys())
    dateindex = np.arange(start_date, end_date, dtype = "datetime64[D]")
    close = np.array([float(stocks[i]["4. close"]) for i in dateindex.astype(str) if i in dates])
    return close


def get_price(symbol, apikey_filename):
    qout = query_time_series_intraday(symbol, apikey_filename)
    stocks = qout["Time Series (1min)"]
    dates = list(stocks.keys())
    current = stocks[dates[0]]["4. close"]
    return current
