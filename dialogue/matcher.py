import os, pprint, yaml, re, random
from .comment import Comment
from .synonym import SynonymIndex
from .response import ResponseIndex


class DialogueMatcher:
    """
    :ivar synonym_index dict
    :ivar matches_index list
    """

    DEFAULT_MATCHES_FILE = 'matches.yml'

    def __init__(self, synonym_index, response_index):

        if not isinstance(synonym_index, SynonymIndex):
            raise Exception('Synonym index is required.')
        if not isinstance(response_index, ResponseIndex):
            raise Exception('Response index is required.')

        self.synonym_index = synonym_index
        self.response_index = response_index

        matches_path = os.path.join(os.path.dirname(__file__), DialogueMatcher.DEFAULT_MATCHES_FILE)
        matches_file = open(matches_path)
        self.matches_index = yaml.load(matches_file, Loader=yaml.Loader)
        matches_file.close()

    def match(self, comment, **kwargs):

        matched_response = None

        if not isinstance(comment, Comment) or comment is None:
            raise Exception('Comment must be a Comment')
        for match_index in self.matches_index:
            regex = self.build_regex(match_index['regex'], match_index['regex_args'], **kwargs)
            m = re.search(regex, comment.comment, re.IGNORECASE)
            if m is not None:
                matched_keyword = random.choice(match_index['response_keyword'])
                matched_response = self.response_index.get_response(keyword=matched_keyword, **kwargs)
                break

        return matched_response

    def build_regex(self, regex, regex_args, **kwargs):
        args = {}
        for key, item in regex_args.items():
            if item.get('synonym') is not None:
                synonym_def = item.get('synonym')
                word_regex = self.synonym_index.get_regex(
                    keyword=synonym_def['keyword'],
                    tags=synonym_def['tags'],
                    is_time_sensitive=synonym_def.get('is_time_sensitive', False))
                args[key] = word_regex
            elif item.get('kwargs') is not None:
                args[key] = kwargs[key]
        regex_str = regex.format(regex, **args)
        return regex_str


