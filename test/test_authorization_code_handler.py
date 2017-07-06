import os
import unittest

import AuthorizationCodeExtractor
from TokenGetter import TokenGetter

class TestAuthorizationCodeExtractor(unittest.TestCase):
    """
    def test_no_data(self):
        token_getter = TokenGetter('tokens.txt')
        access_token, refresh_token = token_getter.getTokens()
        AuthorizationCodeExtractor.setupTokens()
        new_access_token, new_refresh_token = token_getter.getTokens()
        self.assertTrue(new_access_token!=access_token)
        self.assertTrue(new_refresh_token!=refresh_token)
    """
                
if __name__ == '__main__':
    unittest.main()