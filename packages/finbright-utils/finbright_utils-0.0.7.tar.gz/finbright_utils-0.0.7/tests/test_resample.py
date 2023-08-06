from finbright_utils import resample
from finbright_utils.constants.interval import Interval
import yfinance as yf

class Test_resample:

    def test_resample_from_1m(self):
        intervals = Interval()._get_1m_timeframes()
        data = yf.download("BTC-USD", start="2023-02-02", end="2023-02-07", interval = "1m")
        data['time'] = data.index
        data['timestamp'] = data['time'].astype(int)/ 10**9
        data.columns = data.columns.str.lower()
        
        for interval in intervals:
            results = resample.resampling_based_on_time_frame(data, Interval.MIN1, interval)
            source_length = len(data.index)
            dest_length = len(results.index)
            interval_ratio = interval // Interval.MIN1
            data_ratio = source_length // interval_ratio
            assert data_ratio == dest_length
            print("source interval {}, dest interval {} Passed!".format(Interval.MIN1, interval))

    def test_resample_from_1h(self):
        intervals = Interval()._get_1h_timeframes()
        data = yf.download("BTC-USD", start="2023-02-01", end="2023-02-07", interval = "1h")
        data['time'] = data.index
        data['timestamp'] = data['time'].astype(int)/ 10**9
        data.columns = data.columns.str.lower()
        
        for interval in intervals:
            results = resample.resampling_based_on_time_frame(data, Interval.HOUR1, interval)
            source_length = len(data.index)
            dest_length = len(results.index)
            interval_ratio = interval // Interval.HOUR1
            data_ratio = source_length // interval_ratio
            assert data_ratio == dest_length
            print("source interval {}, dest interval {} Passed!".format(Interval.HOUR1, interval))

    def test_resample_from_1d(self):
        intervals = Interval()._get_1d_timeframes()
        data = yf.download("BTC-USD", start="2022-08-02", end="2023-02-01", interval = "1d")
        data['time'] = data.index
        data['timestamp'] = data['time'].astype(int)/ 10**9
        data.columns = data.columns.str.lower()
        
        for interval in intervals:
            results = resample.resampling_based_on_time_frame(data, Interval.DAY1, interval)
            source_length = len(data.index)
            dest_length = len(results.index)
            interval_ratio = interval // Interval.DAY1
            data_ratio = source_length // interval_ratio
            assert data_ratio == dest_length
            print("source interval {}, dest interval {} Passed!".format(Interval.DAY1, interval))


    @staticmethod
    def get_attributes(obj):
        return [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]


tr = Test_resample()
tr.test_resample_from_1d()