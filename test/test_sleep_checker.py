import os
import unittest

import SleepChecker
import ConfigHandler

class TestSleepChecker(unittest.TestCase):

    def test_no_data(self):
        data_location = reduce(
            os.path.join,
            [ConfigHandler.getPath(),'test','TestInfo','SleepCheckerNothing.txt'])
        sleep_checker = SleepChecker.SleepChecker(data_location=data_location)
        self.assertFalse(sleep_checker.isAsleep())
        self.assertTrue(sleep_checker.isAwake())
        
    def test_forged_data_hasnt_woken_up(self):
        data_location = reduce(
            os.path.join,
            [ConfigHandler.getPath(),'test','TestInfo','SleepCheckerAsleep.txt'])
        sleep_checker = SleepChecker.SleepChecker(data_location=data_location)
        self.assertTrue(sleep_checker.isAsleep())
        self.assertFalse(sleep_checker.isAwake())
        
    def test_forged_data_has_woken_up(self):
        data_location = reduce(
            os.path.join,
            [ConfigHandler.getPath(),'test','TestInfo','SleepCheckerWokenUp.txt'])
        sleep_checker = SleepChecker.SleepChecker(data_location=data_location)
        self.assertFalse(sleep_checker.isAsleep())
        self.assertTrue(sleep_checker.isAwake())
                
if __name__ == '__main__':
    unittest.main()