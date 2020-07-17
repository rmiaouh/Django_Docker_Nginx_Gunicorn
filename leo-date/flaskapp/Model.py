import duckling
from pprint import pprint

class Model:
    duckling_model = None

    def __init__(self, language):
        self.duckling_model = duckling.DucklingWrapper(language='fr')


    def get_date_from_sentence(self, sentence):
        return self.duckling_model.parse_time(str(sentence))
