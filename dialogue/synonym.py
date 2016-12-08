import os, yaml, pprint, random, datetime, pytz


class SynonymIndex:

    DEFAULT_SYNONYMS_FILE = 'synonyms.yml'
    TAGS_MATCH_CONTAINS = 'contains'
    TAGS_TIME_SENSITIVE = 'time sensitive'
    TAGS_MORNING = 'morning'
    TAGS_AFTERNOON = 'afternoon'
    TAGS_EVENING = 'evening'
    TAGS_NIGHT = 'night'
    TAGS_SET_TIME_SENSITIVE = {
        TAGS_MORNING,
        TAGS_AFTERNOON,
        TAGS_EVENING,
        TAGS_NIGHT,
    }

    def __init__(self, synonym_index=None):

        if not isinstance(synonym_index, dict) and synonym_index is not None:
            raise Exception('Synonym index must be a dict or None')

        if synonym_index is None:
            synonym_index = {}
        self.index = SynonymIndex.__process_synonyms(synonyms=synonym_index)

        synonyms_path = os.path.join(os.path.dirname(__file__), SynonymIndex.DEFAULT_SYNONYMS_FILE)
        synonyms_file = open(synonyms_path)
        synonyms = yaml.load(synonyms_file, Loader=yaml.Loader)
        default_synonyms = SynonymIndex.__process_synonyms(synonyms)
        self.index = {**self.index, **default_synonyms}
        synonyms_file.close()

    def __process_synonyms(synonyms):

        processed = dict()

        for keyword, words_list in synonyms.items():
            processed[keyword] = []
            for synonyms_dict in words_list:

                processed[keyword].append({
                    'tags': set(synonyms_dict['tags']),
                    'synonyms': set(synonyms_dict['synonyms'])
                })

        return processed

    def get_regex(self, keyword, tags=None, is_time_sensitive=False):

        synonym_set = self.get_synonym_set(keyword=keyword, tags=tags, is_time_sensitive=is_time_sensitive)
        regex = '(' + '|'.join(synonym_set) + ')'
        return regex

    def get_synonym(self, keyword, tags=None, is_time_sensitive=False):

        synonym_set = self.get_synonym_set(keyword=keyword, tags=tags, is_time_sensitive=is_time_sensitive)
        return random.choice(list(synonym_set))

    def get_synonym_set(self, keyword, tags=None, is_time_sensitive=False):

        keyword_dict = self.index[keyword]

        mytz = pytz.timezone(zone='America/Los_Angeles')
        current_datetime = datetime.datetime.now(tz=mytz)
        current_time_tag = SynonymIndex.get_time_tag(current_datetime)
        time_tag_set = SynonymIndex.TAGS_SET_TIME_SENSITIVE.copy()
        time_tag_set.remove(current_time_tag)

        # current_time_sensitive_tag = SynonymIndex.get_time_tag(datetime.time())
        contains_tags_set = set(tags)
        word_set = set()
        for definition_set in keyword_dict:
            if contains_tags_set.issubset(definition_set['tags']):
                if is_time_sensitive is True:
                    if len(time_tag_set & definition_set['tags']) == 0:
                        word_set |= definition_set['synonyms']
                else:
                    word_set |= definition_set['synonyms']

        return word_set

    @classmethod
    def get_time_tag(cls, datetime_obj):

        if 5 <= datetime_obj.hour < 12:
            return cls.TAGS_MORNING
        elif 12 <= datetime_obj.hour < 17:
            return cls.TAGS_AFTERNOON
        elif 17 <= datetime_obj.hour < 22:
            return cls.TAGS_EVENING
        else:
            return cls.TAGS_NIGHT
