import os, yaml, random, pprint, re
from .synonym import SynonymIndex


class ResponseIndex:

    DEFAULT_RESPONSES_FILE = 'responses.yml'
    TAGS_MATCH_CONTAINS = 'contains'

    def __init__(self, response_index=None, synonym_index=None):

        if not isinstance(synonym_index, SynonymIndex):
            raise Exception('Synonym index is required.')
        self.synonym_index = synonym_index

        if not isinstance(response_index, dict) and response_index is not None:
            raise Exception('Response index must be a dict or None')

        if response_index is None:
            response_index = {}
        self.index = self.__process_responses(response_index)

        responses_path = os.path.join(os.path.dirname(__file__), ResponseIndex.DEFAULT_RESPONSES_FILE)
        responses_file = open(responses_path)
        responses = yaml.load(responses_file, Loader=yaml.Loader)
        default_responses = self.__process_responses(responses)
        self.index = {**self.index, **default_responses}
        responses_file.close()

    def __process_responses(self, responses):

        processed = dict()

        for keyword, responses_list in responses.items():
            processed[keyword] = []
            for response in responses_list:
                processed[keyword].append(response)

        return processed

    def get_response(self, keyword, **kwargs):

        response = random.choice(self.index[keyword])
        response_args = {}

        for key, arg in response['response_args'].items():

            if 'synonym' in arg:
                synonym = arg['synonym']

                response_args[key] = self.synonym_index.get_synonym(
                    keyword=synonym['keyword'],
                    tags=synonym['tags'],
                    is_time_sensitive=synonym.get('is_time_sensitive'))
            elif 'kwargs' in arg and arg['kwargs'] is True:

                response_args[key] = kwargs[key]
        response_str = response['response'].format(**response_args)
        return self.capitalize(response_str)

    def uppercase(self, matchobj):
        return matchobj.group(0).upper()

    def capitalize(self,s):
        return re.sub('^([a-z])|[.?!]\s*([a-z])|\s+([a-z])(?=\.)', self.uppercase, s)
