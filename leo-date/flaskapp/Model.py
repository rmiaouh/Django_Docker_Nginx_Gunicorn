import duckling
from pprint import pprint

class Model:
    duckling_model = None

    def __init__(self, language):
        print("model.py ok1")
        self.duckling_model = duckling.DucklingWrapper(language='fr')
        print("model.py ok2")

    def get_date_from_sentence(self, sentence):
        print("model.py ok3")
        return self.duckling_model.parse_time(str(sentence))
        print("model.py ok4")
