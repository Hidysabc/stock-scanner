import numpy as np
import json
import requests
import datetime
import pandas as pd

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
    #stocks = json.load(open(f,"r"))
    stocks = query_time_series_daily(symbol, apikey_filename)
    k = list(stocks.keys())
    stocks = stocks[k[-1]]
    dates = list(stocks.keys())
    start_date_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    span = int((end_date_parse - start_date_parse)/datetime.timedelta(1))
    dateindex = pd.date_range(start_date,periods = span, freq = "D")
    close = np.array([float(stocks[i]["4. close"]) for i in dateindex.astype(str) if i in dates])
    #close = np.array([float(stocks[i]["4. close"]) for i in stocks])
    #start_date_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    #end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    #span = int((end_date_parse - start_date_parse)/datetime.timedelta(1))
    #dateindex = pd.date_range(start_date,periods = span, freq = "D")
    #close = [close[i] for i in dateindex.astype(str) if i in dates]
    #close = close[dates.index(end_date):dates.index(start_date)]
    #print(close)
    return close

def get_price(symbol, apikey_filename):
    #stocks = json.load(open(f,"r"))
    stocks = query_time_series_intraday(symbol, apikey_filename)
    k = list(stocks.keys())
    stocks = stocks[k[-1]]
    dates = list(stocks.keys())
    current = stocks[dates[0]]["4. close"]
    #print(current)
    return current
