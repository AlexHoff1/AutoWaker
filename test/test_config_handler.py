import unittest
import os

import ConfigHandler

class TestConfigHandler(unittest.TestCase):
    
    def test_path_exists(self):
        path = ConfigHandler.getPath()
        self.assertTrue(os.path.exists(path))
        
    
if __name__ == '__main__':
    unittest.main()