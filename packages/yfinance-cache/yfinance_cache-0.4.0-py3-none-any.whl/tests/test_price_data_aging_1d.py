import unittest

from .context import yfc_dat as yfcd
from .context import yfc_time as yfct

from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo

from pprint import pprint

## 2022 calendar:
## X* = day X is USA public holiday that closed NYSE
##  -- February --
##  Mo   Tu   We   Th   Fr   Sa   Su
##  7    8    9    10   11   12   13
##  14   15   16   17   18   19   20
##  21*  22   23   24   25   26   27
##  28

class Test_PriceDataAging_1D(unittest.TestCase):

    def setUp(self):
        self.market = "us_market"
        self.exchange = "NMS"
        self.market_tz = ZoneInfo('US/Eastern')
        self.market_open_time  = time(hour=9, minute=30)
        self.market_close_time = time(hour=16, minute=0)

        self.monday  = date(year=2022, month=2, day=14)
        self.tuesday = date(year=2022, month=2, day=15)
        self.friday  = date(year=2022, month=2, day=18)
        self.saturday= date(year=2022, month=2, day=19)

    ## Test day interval fetched same day
    def test_sameDay(self):
        interval = yfcd.Interval.Days1

        intervalStartD = self.monday

        max_ages = []
        fetch_dts = []
        dt_nows = []
        expire_on_candle_closes = []
        yf_lags = []
        answers = []

        fetch_dts.append(datetime.combine(self.monday, time(hour=12, minute=5),  self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.monday, time(hour=12, minute=34), self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(False)

        fetch_dts.append(datetime.combine(self.monday, time(hour=12, minute=5),  self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.monday, time(hour=12, minute=35), self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(True)



        fetch_dts.append(datetime.combine(self.monday, time(hour=12, minute=5),  self.market_tz))
        max_ages.append(timedelta(minutes=60))
        dt_nows.append(  datetime.combine(self.monday, time(hour=13, minute=4), self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(False)

        fetch_dts.append(datetime.combine(self.monday, time(hour=12, minute=5),  self.market_tz))
        max_ages.append(timedelta(hours=1))
        dt_nows.append(  datetime.combine(self.monday, time(hour=13, minute=5), self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(True)



        fetch_dts.append(datetime.combine(self.monday, time(hour=23, minute=55), self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.tuesday, time(hour=0, minute=0),  self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(False)

        fetch_dts.append(datetime.combine(self.monday, time(hour=23, minute=55), self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.tuesday, time(hour=0, minute=0),  self.market_tz))
        expire_on_candle_closes.append(True) ; yf_lags.append(timedelta(minutes=0))
        answers.append(True)

        fetch_dts.append(datetime.combine(self.monday, time(hour=23, minute=55), self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.tuesday, time(hour=0, minute=0),  self.market_tz))
        expire_on_candle_closes.append(True) ; yf_lags.append(timedelta(minutes=1))
        answers.append(False)

        fetch_dts.append(datetime.combine(self.monday, time(hour=23, minute=55), self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.tuesday, time(hour=0, minute=1),  self.market_tz))
        expire_on_candle_closes.append(True) ; yf_lags.append(timedelta(minutes=1))
        answers.append(True)



        fetch_dts.append(datetime.combine(self.monday,  time(hour=23, minute=55), self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.tuesday, time(hour=9,  minute=0),  self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(False)

        fetch_dts.append(datetime.combine(self.monday,  time(hour=23, minute=55), self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.tuesday, time(hour=9, minute=30),  self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(False)

        fetch_dts.append(datetime.combine(self.monday,  time(hour=23, minute=55), self.market_tz))
        max_ages.append(timedelta(minutes=30))
        dt_nows.append(  datetime.combine(self.tuesday, time(hour=9, minute=30),  self.market_tz))
        expire_on_candle_closes.append(True) ; yf_lags.append(timedelta(0))
        answers.append(True)

        for i in range(len(fetch_dts)):
            fetch_dt = fetch_dts[i]
            max_age = max_ages[i]
            dt_now = dt_nows[i]
            expire_on_candle_close = expire_on_candle_closes[i]
            yf_lag = yf_lags[i]
            answer = answers[i]
            response = yfct.IsPriceDatapointExpired(intervalStartD, fetch_dt, max_age, self.exchange, interval, triggerExpiryOnClose=expire_on_candle_close, yf_lag=yf_lag, dt_now=dt_now)
            try:
                self.assertEqual(response, answer)
            except:
                print("fetch_dt = {0}".format(fetch_dt))
                print("expire_on_candle_close = {}".format(expire_on_candle_close))
                print("yf_lag = {}".format(yf_lag))
                print("max_age = {0}".format(max_age))
                print("dt_now = {0}".format(dt_now))
                print("answer:")
                pprint(answer)
                print("response:")
                pprint(response)
                raise

    ## Test day interval fetched same day, on exchange with data delay
    def test_sameDay_delay(self):
        exchange = "LSE" # 20min delay
        yf_lag = timedelta(minutes=20)
        market_tz = ZoneInfo("Europe/London")
        interval = yfcd.Interval.Days1
        market_open = time(8)
        market_close = time(16, 30)

        ## Just before interval close, but with data delay was fetched after close:
        interval_close_dt = datetime.combine(self.tuesday, time(0), market_tz)
        fetch_dt = interval_close_dt + timedelta(minutes=1)
        intervalStart = self.monday
        max_age = timedelta(minutes=10)
        dt_now = interval_close_dt + timedelta(minutes=14)
        expire_on_candle_close = False
        answer = True
        result = yfct.IsPriceDatapointExpired(intervalStart, fetch_dt, max_age, exchange, interval, triggerExpiryOnClose=expire_on_candle_close, yf_lag=yf_lag, dt_now=dt_now)
        try:
            self.assertEqual(result, answer)
        except:
            print("result:")
            pprint(result)
            print("answer:")
            pprint(answer)
            raise
        #
        dt_now = interval_close_dt + timedelta(minutes=2)
        answer = False
        result = yfct.IsPriceDatapointExpired(intervalStart, fetch_dt, max_age, exchange, interval, triggerExpiryOnClose=expire_on_candle_close, yf_lag=yf_lag, dt_now=dt_now)
        try:
            self.assertEqual(result, answer)
        except:
            print("result:")
            pprint(result)
            print("answer:")
            pprint(answer)
            raise

        ## Check that 'expire-on-candle-close' still works:
        fetch_dt = datetime.combine(self.monday, time(23,59), market_tz)
        dt_now = datetime.combine(self.tuesday, time(0), market_tz) + yf_lag + timedelta(minutes=1)
        max_age = timedelta(hours=1)
        expire_on_candle_close = True
        answer = True
        result = yfct.IsPriceDatapointExpired(intervalStart, fetch_dt, max_age, exchange, interval, triggerExpiryOnClose=expire_on_candle_close, yf_lag=yf_lag, dt_now=dt_now)
        try:
            self.assertEqual(result, answer)
        except:
            print("result:")
            pprint(result)
            print("answer:")
            pprint(answer)
            raise

        ## Just after market close + data delay:
        fetch_dt = interval_close_dt + yf_lag + timedelta(minutes=1)
        intervalStart = self.monday
        max_age = timedelta(minutes=10)
        dt_now = interval_close_dt + yf_lag + timedelta(minutes=14)
        expire_on_candle_close = False
        answer = False
        result = yfct.IsPriceDatapointExpired(intervalStart, fetch_dt, max_age, exchange, interval, triggerExpiryOnClose=expire_on_candle_close, yf_lag=yf_lag, dt_now=dt_now)
        try:
            self.assertEqual(result, answer)
        except:
            print("result:")
            pprint(result)
            print("answer:")
            pprint(answer)
            raise

        ## Just after interval close + data delay:
        fetch_dt = datetime.combine(self.tuesday, time(0), market_tz) + yf_lag + timedelta(minutes=1)
        intervalStart = self.monday
        max_age = timedelta(minutes=10)
        dt_now = datetime.combine(self.monday, market_close, market_tz) + yf_lag + timedelta(minutes=14)
        expire_on_candle_close = False
        answer = False
        result = yfct.IsPriceDatapointExpired(intervalStart, fetch_dt, max_age, exchange, interval, triggerExpiryOnClose=expire_on_candle_close, yf_lag=yf_lag, dt_now=dt_now)
        try:
            self.assertEqual(result, answer)
        except:
            print("result:")
            pprint(result)
            print("answer:")
            pprint(answer)
            raise

    ## Test Friday interval fetched same day when dt_now is next day (weekend)
    def test_nextDayWeekend(self):
        interval = yfcd.Interval.Days1
        intervalStart = self.friday

        max_ages = []
        fetch_dts = []
        dt_nows = []
        expire_on_candle_closes = []
        yf_lags = []
        answers = []

        max_ages.append(timedelta(minutes=30))
        fetch_dts.append(datetime.combine(self.friday,   time(hour=14, minute=55), self.market_tz))
        dt_nows.append(  datetime.combine(self.saturday, time(hour=9, minute=10), self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(True)

        max_ages.append(timedelta(minutes=30))
        fetch_dts.append(datetime.combine(self.friday,   time(hour=23, minute=55), self.market_tz))
        dt_nows.append(  datetime.combine(self.saturday, time(hour=9, minute=10), self.market_tz))
        expire_on_candle_closes.append(False) ; yf_lags.append(timedelta(0))
        answers.append(False)

        max_ages.append(timedelta(minutes=30))
        fetch_dts.append(datetime.combine(self.friday,   time(hour=23, minute=55), self.market_tz))
        dt_nows.append(  datetime.combine(self.saturday, time(hour=9, minute=10), self.market_tz))
        expire_on_candle_closes.append(True) ; yf_lags.append(timedelta(0))
        answers.append(True)

        for i in range(len(fetch_dts)):
            fetch_dt = fetch_dts[i]
            max_age = max_ages[i]
            dt_now = dt_nows[i]
            expire_on_candle_close = expire_on_candle_closes[i]
            yf_lag = yf_lags[i]
            answer = answers[i]
            response = yfct.IsPriceDatapointExpired(intervalStart, fetch_dt, max_age, self.exchange, interval, triggerExpiryOnClose=expire_on_candle_close, yf_lag=yf_lag, dt_now=dt_now)
            try:
                self.assertEqual(response, answer)
            except:
                print("fetch_dt = {0}".format(fetch_dt))
                print("max_age = {0}".format(max_age))
                print("dt_now = {0}".format(dt_now))
                print("answer:")
                pprint(answer)
                print("response:")
                pprint(response)
                raise

if __name__ == '__main__':
    unittest.main()
