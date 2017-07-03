import os
import unittest

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover(os.path.join('.','test'))
    unittest.TextTestRunner(verbosity=1).run(testsuite)