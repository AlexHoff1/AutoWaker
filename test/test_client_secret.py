import unittest

import ClientSecretExtractor

class TestTimeHandler(unittest.TestCase):

    def test_client_secret_not_null(self):
        secret = ClientSecretExtractor.getClientSecret()
        self.assertTrue(secret!=None and secret!='')
    
    def test_client_secret_type_and_size(self):
        secret = ClientSecretExtractor.getClientSecret()
        self.assertTrue(type(secret)==str)
        self.assertTrue(len(secret)>=10)


if __name__ == '__main__':
    unittest.main()