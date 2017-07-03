import os
import unittest

import TokenGetter

class TestTokenGetter(unittest.TestCase):

    def test_get_token(self):
        getter = TokenGetter.TokenGetter(reduce(os.path.join, ['test','TestInfo','FakeTokens.txt']))
        access_token, refresh_token = getter.getTokens()
        self.assertEqual(access_token,'catand')
        self.assertEqual(refresh_token,'dog')
    
    def test_raise_invalid_location(self):
        location = reduce(os.path.join, ['test','TestInfo','FakeTokensDNE.txt'])
        getter = TokenGetter.TokenGetter(location)
        if os.path.exists(location):
            try:
                os.remove(location)
            except:
                return #Can't run this test...
        else:
            with self.assertRaises(IOError):
                access_token, refresh_token = getter.getTokens()
    
    def test_empty_tokens(self):
        getter = TokenGetter.TokenGetter(reduce(os.path.join, ['test','TestInfo','FakeBlankTokens.txt']))
        access_token, refresh_token = getter.getTokens()
        self.assertEqual(access_token,'')
        self.assertEqual(refresh_token,'')
    
    def test_blank_file(self):
        getter = TokenGetter.TokenGetter(reduce(os.path.join, ['test','TestInfo','FakeTokensFileNoContent.txt']))
        access_token, refresh_token = getter.getTokens()
        self.assertEqual(access_token, '')
        self.assertEqual(refresh_token, '')
    
    def test_one_token_file(self):
        getter = TokenGetter.TokenGetter(reduce(os.path.join, ['test','TestInfo','FakeTokensFileOneToken.txt']))
        access_token, refresh_token = getter.getTokens()
        self.assertEqual(access_token, 'catand')
        self.assertEqual(refresh_token, '')
    
    def test_set_tokens_existing_file(self):
        location = reduce(os.path.join, ['test','TestInfo','FakeTokensWriteable.txt'])
        if os.path.exists(location):
            os.remove(location)
        #Clean the file just in case this test existed randomly.
        file_fake = open(location,'w')
        file_fake.close()
        access_token_info = 'cats are cool'
        refresh_token_info = 'but dogs are baws.'
        getter = TokenGetter.TokenGetter(location)
        getter.setTokens(access_token = access_token_info, refresh_token = refresh_token_info)
        file_real = open(location,'r')
        access_token = file_real.readline().strip()
        refresh_token = file_real.readline().strip()
        self.assertEqual(access_token, access_token_info)
        self.assertEqual(refresh_token, refresh_token_info)
        
    def test_set_tokens_no_config_file(self):
        location = reduce(os.path.join, ['test','TestInfo','FakeTokensWriteable.txt'])
        if os.path.exists(location):
            os.remove(location)
        #Clean the file just in case this test existed randomly.
        access_token_info = 'cats are cool'
        refresh_token_info = 'but dogs are baws.'
        getter = TokenGetter.TokenGetter(location)
        getter.setTokens(access_token = access_token_info, refresh_token = refresh_token_info)
        file_real = open(location,'r')
        access_token = file_real.readline().strip()
        refresh_token = file_real.readline().strip()
        self.assertEqual(access_token, access_token_info)
        self.assertEqual(refresh_token, refresh_token_info)
    
    #This one is hard to implement because it needs actual tokens :\.
    def test_refresh_tokens_does_not_return_same_tokens(self):
        return
        
        
if __name__ == '__main__':
    unittest.main()