import unittest
import os

import ConfigHandler
import DataWriter

class TestDataWriter(unittest.TestCase):
    
    def test_write_to_location(self):
        test_path = reduce(os.path.join,[ConfigHandler.getPath(),'test','TestInfo'])
        self.assertTrue(os.path.exists(test_path)) 
        junk_location = os.path.join(test_path, 'junk.txt') 
        DataWriter.writeDataToFile(data = 'myjunk', location = junk_location)
        file_opened = open(junk_location, 'r')
        self.assertEquals('myjunk',file_opened.read())
        file_opened.close()
        os.remove(junk_location)
        
    def test_write_to_directory_that_dne(self):
        test_path = reduce(os.path.join,[ConfigHandler.getPath(),'test','TestInfo'])
        test_path_2 = os.path.join(test_path, 'NewPathThatDNE')
        junk_location_2 = os.path.join(test_path_2,'junk.txt')
        DataWriter.writeDataToFile(data = 'myjunk', location = junk_location_2)
        file_opened = open(junk_location_2,'r')
        self.assertEquals('myjunk',file_opened.read())
        file_opened.close()
        os.remove(junk_location_2)
        os.rmdir(test_path_2)
    
    def test_null_location_does_not_write(self):
        test_path = ''
        result = DataWriter.writeDataToFile(data = 'myjunk', location = test_path)
        self.assertFalse(result)
    
    #  Makes sure that the data can't write to places where permissions fail.
    def test_root_fails(self):
        test_path = os.path.join('','/')
        result = DataWriter.writeDataToFile(data = 'myjunk', location = test_path)
        self.assertFalse(result)
        
if __name__ == '__main__':
    unittest.main()