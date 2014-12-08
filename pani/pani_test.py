import os
import pani
import unittest
import tempfile

class PaniTestCase(unittest.TestCase):

    def setUp(self):
        pani.app.config['TESTING'] = True
        self.app = pani.app.test_client()

    def tearDown(self):
        pass

    def test_first(self):
        assert (1 + 1) == 2

    def test_second(self):
        assert (1 + 2) == 2



if __name__ == '__main__':
    unittest.main()
