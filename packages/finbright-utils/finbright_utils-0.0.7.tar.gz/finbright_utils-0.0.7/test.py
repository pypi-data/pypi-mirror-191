from finbright_utils.fin_statistics import correlation, resample
from finbright_utils.constants.interval import Interval
import pandas as pd
import yfinance as yf
import datetime 
import numpy as np


def test_resample_from_1m():
    data = yf.download("BTC-USD", start="2023-02-02", end="2023-02-07", interval = "1m")
    data5m = yf.download("BTC-USD", start="2023-02-02", end="2023-02-07", interval = "5m")
    data['time'] = data.index
    data['timestamp'] = data['time'].astype(int)/ 10**9
    data.columns = data.columns.str.lower()
    results = resample.resampling_based_on_time_frame(data, Interval.MIN1, Interval.MIN5)
    

test_resample_from_1m()
    # for interval in intervals:
    #     results = resample.resampling_based_on_time_frame(data, Interval.MIN1, interval)
    #     source_length = len(data.index)
    #     dest_length = len(results.index)
    #     interval_ratio = interval // Interval.MIN1
    #     data_ratio = source_length // interval_ratio
    #     assert data_ratio == dest_length
    #     print("source interval {}, dest interval {} Passed!".format(Interval.MIN1, interval))
        
# min1_data_aapl = yf.download("AAPL", start="2023-01-31", end="2023-02-01", interval = "1m")["Adj Close"]
# min1_data_msf = yf.download("MSFT", start="2023-01-31", end="2023-02-01", interval = "1m")["Adj Close"]
# corr = correlation(min1_data_aapl, min1_data_msf)
# print(corr)

# hour1_data = yf.download("MSFT", start="2023-01-01", end="2023-02-01", interval = "1h")
# hour1_data.drop(["Adj Close"], axis=1, inplace=True)
# hour1_data['datetime'] = pd.to_datetime(hour1_data.index)
# hour1_data["timestamp"] = [datetime.timestamp() for datetime in hour1_data["datetime"]]
# hour1_data.reset_index(inplace=True)

# print(hour1_data)
# hour1_data.rename(columns={'Open': 'open',
#                 'High': 'high',
#                 'Low': 'low',
#                 'Close': 'close',
#                 'Volume': 'volume',
#                     },
#         inplace=True, errors='raise')
# hour1_data["timestamp"] = hour1_data.datetime.timestamp()
# min1_data.index = pd.to_datetime(min1_data.index)
# print(min1_data["Datetime"])
# hour1_data['timestamp'] = hour1_data["timestamp"].values.astype(np.int64) // 10 ** 9


# day1_data = resample.resampling_based_on_time_frame(hour1_data, Interval.HOUR1, Interval.DAY1)
# print(day1_data)

