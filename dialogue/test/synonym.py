import unittest, pprint, datetime, pytz
from ..synonym import SynonymIndex
from ddt import ddt, data, unpack


@ddt
class SynonymIndexTestCase(unittest.TestCase):

    def setUp(self):
        self.synonym_index = SynonymIndex()

    def test_get_synonym(self):
        tags = ['how do you do', 'interjection']

        synonym = self.synonym_index.get_synonym(keyword='hello', tags=tags, is_time_sensitive=True)
        self.assertIsNotNone(synonym)
        self.assertGreater(len(synonym), 0, "Length of hello synonym should be greater than zero")

    @data((10, SynonymIndex.TAGS_MORNING), (13, SynonymIndex.TAGS_AFTERNOON),
          (20, SynonymIndex.TAGS_EVENING), (23, SynonymIndex.TAGS_NIGHT))
    @unpack
    def test_synonym_get_timezone_tag(self, hour, expected_tag):
        mytz = pytz.timezone(zone='America/Los_Angeles')
        current_time = datetime.datetime.now(tz=mytz)
        current_time = current_time.replace(hour=hour)
        current_tag = SynonymIndex.get_time_tag(current_time)
        self.assertEqual(current_tag, expected_tag)

    def tearDown(self):
        del self.synonym_index