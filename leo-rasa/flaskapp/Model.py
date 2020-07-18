from rasa.nlu.model import Interpreter
import pandas as pd


class Model:
    nlp_model = None

    def __init__(self, bot_id, language):
        self.nlp_model = Interpreter.load(
            f"./model/{bot_id}/{language}",
            skip_validation=True)

    def get_intents_from_sentence(self, sentence):
        result = self.nlp_model.parse(sentence)
        return result

