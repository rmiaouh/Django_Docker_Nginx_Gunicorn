import sys, json, unicodedata, re, string, codecs
from collections import defaultdict
import spacy


class Model:
    whitelist_words = []
    blacklist_words = []
    nlp_model = None

    def __init__(self, language):
        # Initialize the model
        self.nlp_model = spacy.load("./fr_model")

        # Import whitelist_words
        with codecs.open("./assets/whitelist.txt", encoding='utf8') as f:
            whitelist_data = f.read()
            self.whitelist_words = whitelist_data.split('\n')

        # Import blacklist_words
        with codecs.open("./assets/blacklist.txt", encoding='utf8') as f:
            blacklist_data = f.read()
            self.blacklist_words = blacklist_data.split('\n')

    def remove_accents(self, sentence):
        """
            Remove accents from a string
            Parameters
            ----------
            sentence : str
                The sentence wich will be parsed
            Returns
            -------
            str
                The sentence cleaned from it's accents
        """

        return ''.join(char for char in unicodedata.normalize('NFD', sentence)
                       if unicodedata.category(char) != 'Mn')

    def remove_punctuations(self, sentence):
        """
            Remove punctuations from a string
            Parameters
            ----------
            sentence : str
                The sentence wich will be parsed
            Returns
            -------
            str
                The sentence cleaned from it's punctuations
        """

        replaced = sentence.translate(
            str.maketrans(
                string.punctuation,
                ' '*len(string.punctuation)
            )
        )

        return " ".join(replaced.split())  # Remove double spaces

    def remove_blacklist_words(self, sentence):
        """
            Remove a list of words from a string
            Parameters
            ----------
            sentence : str
                The sentence wich will be parsed
            Returns
            -------
            str
                The sentence cleaned from it's words
        """

        words_filtered = [word for word in sentence.split()
                          if word not in self.blacklist_words]

        return (" ").join(words_filtered)

    def clean_entities(self, entities):
        """
            Keep from an list of spacy entities only ones which match some
            requirements. Also change the entities list to a dictionnary with
            entities group by their labels.
            Parameters
            ----------
            entities : list
                The list of spacy entities
            Returns
            -------
            dic
                Cleaned entities organized by their label (adress, cp, ...)
        """

        clean_entities = defaultdict(list)

        for entity in entities:
            try:
                if entity.label_ == "cp":
                    # If the postal code does not match regular format
                    if len(entity.text) != 5:
                        continue

                    # If it's a postal code
                    if all([char.isdigit() for char in entity.text]) is True:
                        clean_entities[entity.label_].append(entity.text)

                # Check for each label if the adress is valid
                elif entity.label_ != "v5":
                    # Don't keep a string that has less than 4 characters
                    if len(entity.text) <= 3:
                        continue

                    # Don't keep a string that has only digits
                    if all([char.isdigit() for char in entity.text]) is True:
                        continue

                    # Only keep if there is a white listed word in the string
                    for word in entity.text.split():
                        if word in self.whitelist_words:
                            clean_entities[entity.label_].append(entity.text)
                            break
            except Exception as e:
                print(str(e))
                return json.dumps({})

        return clean_entities

    def get_addresses_from_sentence(self, sentence):
        # Clean the sentence before using it
        sentence = self.remove_accents(sentence)
        sentence = self.remove_punctuations(sentence)
        sentence = self.remove_blacklist_words(sentence)

        doc = self.nlp_model(sentence)

        return self.clean_entities(doc.ents)
