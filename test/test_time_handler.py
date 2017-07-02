import unittest
import datetime
import TimeHandler

class TestTimeHandler(unittest.TestCase):

    def test_addHours(self):
        dt = datetime.datetime(2015,10,1,0,0,0)
        self.assertEqual(TimeHandler.addHours(dt,6), datetime.datetime(2015,10,1,6,0,0))
        


if __name__ == '__main__':
    unittest.main()