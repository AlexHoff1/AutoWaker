import datetime
import time
import unittest

import TimeHandler

class TestTimeHandler(unittest.TestCase):

    def test_addHours(self):
        dt = datetime.datetime(2015,10,1,0,0,0)
        self.assertEqual(TimeHandler.addHours(dt,6), datetime.datetime(2015,10,1,6,0,0))
    
    def test_checkTimes(self):
        end_datetime = TimeHandler.endCheckTime()
        start_datetime = TimeHandler.startCheckTime()
        end_greater_than_start = end_datetime>start_datetime
        self.assertTrue(end_greater_than_start)

    def test_now_is_close(self):
        actual_now_according_to_library = datetime.datetime.now().time()
        time_handler_now = TimeHandler.now()
        dummy_date = datetime.date(2000,1,1)
        dt1 = datetime.datetime.combine(dummy_date, time_handler_now)
        dt2 = datetime.datetime.combine(dummy_date, actual_now_according_to_library)
        difference_in_times = dt1 - dt2  #dt1 should always be > dt2, or it's in the future.
        is_within_a_minute = difference_in_times<=datetime.timedelta(seconds=60)
        self.assertTrue(is_within_a_minute)
    
    #  This will be useful to have when today() implementation changes to account for day shifts.
    def test_today(self):
        yesterday = datetime.date.today() - datetime.timedelta(1)
        today_according_to_handler = TimeHandler.today()
        is_reasonable = (
            today_according_to_handler == yesterday.strftime('%Y-%m-%d') or
            today_according_to_handler == datetime.date.today().strftime('%Y-%m-%d'))
        self.assertTrue(is_reasonable)
    
    def test_format_consistency(self):
        today_according_to_timehandler = TimeHandler.today()
        clocktime_according_to_timehandler = TimeHandler.clocktime()
        self.assertTrue(type(clocktime_according_to_timehandler)==str)
        self.assertTrue(type(today_according_to_timehandler)==str)
        parse_date = datetime.datetime.strptime(today_according_to_timehandler, '%Y-%m-%d')
        parse_time = datetime.datetime.strptime(clocktime_according_to_timehandler, "%H:%M:%S")
        self.assertTrue(type(parse_date)==datetime.datetime)
        self.assertTrue(type(parse_time)==datetime.datetime)

if __name__ == '__main__':
    unittest.main()