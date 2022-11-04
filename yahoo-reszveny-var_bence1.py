import math
import json
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from scipy import stats


def varfunc(symbol, confidence, date_start, date_end):

    
    timestamp_start = int(date_start.timestamp())
    timestamp_end = int(date_end.timestamp())
    
    url_template = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1={period1}&period2={period2}&interval=1d"
    
    url = url_template.format(symbol = symbol, period1=timestamp_start, period2=timestamp_end)
    
    response = requests.get(url)
    data = json.loads(response.content)
    
    timestamp = data["chart"]["result"][0]["timestamp"]
    values = data["chart"]["result"][0]["indicators"]["quote"][0]
    
    dates = []
    for t in timestamp:
        dates.append(datetime.fromtimestamp(t))
    
    stocks = pd.DataFrame(values, index=dates)
    
    stocks["close"].plot.line()
    
    stocks["loghozam"] = np.log(stocks["close"]/stocks["close"].shift(1))
    
    stocks = stocks[1:].copy()
    
    standard_deviation = stocks["loghozam"].std()
    
    mean = stocks["loghozam"].mean()
    
    VaR = stats.norm.ppf(confidence, scale=standard_deviation)
    return mean/abs(VaR)

date_start = datetime(2018,11,7)
date_end =datetime(2019,11,7)

#nflix = varfunc("NFLX", 0.99, date_start, date_end)
#print(nflix)


with open("adatok/nasdq.txt", ) as inf:
    nasdaq_stock = inf.read().splitlines()

max_score = -99999
best_stock =None    

for stock in nasdaq_stock:
        score_value = varfunc(stock, 0.99, date_start, date_end)
        if score_value > max_score:
            max_score = score_value
            best_stock = stock

print(best_stock, max_score)

scores = []
for stock in nasdaq_stock:
    score_value=varfunc(stock, 0.99, date_start, date_end)
    scores.append(score_value)
    
print(nasdaq_stock[np.argmax(scores)])
        
