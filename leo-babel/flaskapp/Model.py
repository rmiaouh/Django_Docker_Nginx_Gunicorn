import os
import spacy
from spacy_langdetect import LanguageDetector


class Model:
    nlp_model = None
    supported_languages = None

    def __init__(self):
        # Initialize the model
        self.nlp_model = spacy.load('en')

        # Load language detector module in our model
        self.nlp_model.add_pipe(
            LanguageDetector(),
            name='language_detector',
            last=True)

        self.supported_languages = ['fr','en']

    def get_language_from_sentence(self, sentence):
        # Minimum sentence length prevent language detection to be triggered
        # for banalities like "hello", "thank you", ...
        min_sentence_length = 5
        if len(str(sentence).split()) < min_sentence_length:
            return {"error": "sentence too short"}

        doc = self.nlp_model(str(sentence))
        language_object = (doc._.language)

        # Don't keep detections which doesn't match a high confidence score
        min_confidence = 0.8
        if float(language_object['score']) < min_confidence:
            return {"error": "not_enough_confidence"}

        # Don't keep detections from unsupported languages
        if language_object['language'] not in self.supported_languages:
            return {"error": "not_supported_language"}

        return language_object
