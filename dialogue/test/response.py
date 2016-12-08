import unittest, pprint
from ..response import ResponseIndex
from ..synonym import SynonymIndex


class ResponseIndexTestCase(unittest.TestCase):

    def setUp(self):
        synonym_index = SynonymIndex()
        self.response_index = ResponseIndex(synonym_index=synonym_index)

    def test_hello_response(self):
        responses = self.response_index.index.get('hello')
        self.assertIsNotNone(responses)
        self.assertGreater(len(responses), 0, "Length of hello responses should be greater than zero")

    def test_response_index_get_random(self):
        hello_response = self.response_index.get_response(keyword='hello', commenter_name='Bob')

        self.assertTrue(isinstance(hello_response, str))
        self.assertGreater(len(hello_response), 0, "Length of hello response string should be greater than zero")

    def tearDown(self):
        del self.response_index
