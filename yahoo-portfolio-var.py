# -*- coding: utf-8 -*-
import math
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from scipy import stats

now = datetime.now()
date_start = datetime(2018,10,23)
date_end = datetime(2019,10,22)
timestamp_start = int(date_start.timestamp())
timestamp_end = int(date_end.timestamp())

url_template = "https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1={1}&period2={2}&interval=1d"

all_symbols = None

for symbol in ["FB", "AMZN", "AAPL", "NFLX", "GOOG"]:
    response = requests.get(url_template.format(symbol, timestamp_start, timestamp_end))
    response_json = response.json()
    dates = []
    for timestamp in response_json["chart"]["result"][0]["timestamp"]:
        dates.append(datetime.fromtimestamp(timestamp))
    data = response_json["chart"]["result"][0]["indicators"]["quote"][0]
    symbol_data = pd.DataFrame(data, index=dates)
    for column in symbol_data.columns:
        symbol_data = symbol_data.rename(columns={column: symbol+"_"+column})
    if all_symbols is None:
        all_symbols = symbol_data
    else:
        all_symbols = pd.concat([all_symbols, symbol_data], axis=1)

for symbol in ["FB", "AMZN", "AAPL", "NFLX", "GOOG"]:
    all_symbols[symbol+"_close_loghozam"] = np.log(all_symbols[symbol+"_close"]/all_symbols[symbol+"_close"].shift(1))

all_symbols["FB_close_loghozam"].mean()
loghozamok = all_symbols[1:][["FB_close_loghozam", "AMZN_close_loghozam", "AAPL_close_loghozam", "NFLX_close_loghozam", "GOOG_close_loghozam"]]
covariance_matrix = loghozamok.cov()
portfolio_variance = np.dot(np.array([0.2]*5).T, covariance_matrix)
portfolio_variance = np.dot(portfolio_variance, np.array([0.2]*5))
standard_deviation = math.sqrt(portfolio_variance)
VaR = stats.norm.ppf(0.99, scale=standard_deviation)
