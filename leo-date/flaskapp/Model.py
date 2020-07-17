import duckling
from pprint import pprint


class Model:
    duckling_model = None

    def __init__(self, language):
        print("ok11")

        self.duckling_model = duckling.DucklingWrapper(language='fr')
        print("ok12")

    def get_date_from_sentence(self, sentence):
        print("ok13")
        return self.duckling_model.parse_time(str(sentence))
