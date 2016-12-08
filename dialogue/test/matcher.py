import unittest, pprint, datetime, pytz
from ..synonym import SynonymIndex
from ..response import ResponseIndex
from ..matcher import DialogueMatcher
from ..comment import Comment
from ddt import ddt, data, unpack


@ddt
class DialogueMatcherTestCase(unittest.TestCase):

    def setUp(self):
        self.synonym_index = SynonymIndex()
        self.response_index = ResponseIndex(synonym_index=self.synonym_index)
        self.matcher = DialogueMatcher(synonym_index=self.synonym_index, response_index=self.response_index)

    def test_get_match(self):

        comment = Comment(comment='Hello Bender')
        match = self.matcher.match(comment=comment, commenter_name='Bob', commentee_name='Bender')
        self.assertIsNotNone(match)
        self.assertGreater(len(match), 0, "Length of hello matches should be greater than zero")

    def tearDown(self):
        del self.synonym_index
        del self.response_index
        del self.matcher
