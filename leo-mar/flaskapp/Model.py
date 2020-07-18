import os, unicodedata
import spacy
from collections import defaultdict
import pandas as pd
from difflib import SequenceMatcher
import edlib


class Model:
    nlp_model = None
    csv_dataframe = None
    blacklist_words = None

    def __init__(self, bot_id, language):
        self.nlp_model = spacy.load(f"./model/{bot_id}")

        self.csv_dataframe = pd.read_csv(
            f"./model/{bot_id}/finalized.csv",
            sep=",",
            names=['word', 'id', 'category']
        )
        self.blacklist_words = pd.read_csv(
            f"./assets/{language}_banwords.csv",
            sep=",",
            names=['word']
        )["word"].tolist()


    def get_appellations_from_sentence(self, sentence):
        # Clean the sentence before using it
        sentence = sentence.lower()
        sentence = self.remove_accents(sentence)
        sentence = self.remove_blacklist_words(sentence)

        # call model
        doc = self.nlp_model(sentence)

        entities = defaultdict(list)
        for ent in doc.ents:
            entities[ent.label_].append(ent.text)

        final = []
        for category, values in entities.items():
            # Split dataframe into a specific dataframe to this category
            category_dataframe = (
                self.csv_dataframe
                .loc[self.csv_dataframe['category'] == category]
            )

            if category_dataframe.empty:
                continue

            for value in values:
                # Order dataframe words by their similarity to the model value
                # and only keep the most similar
                dataframe_word = category_dataframe['word']
                closest_value = self.find_closest_value(dataframe_word, value)

                # Convert the simmilarity between the word and the model value
                # to a ratio If it's simmilarity is not enough, skip it
                min_similarity = 0.55
                similarity = (SequenceMatcher(None, closest_value, value)
                              .ratio())

                if similarity < min_similarity:
                    continue

                # Get the dataframe line of the closest_value
                line_data = (
                    category_dataframe
                    .loc[category_dataframe['word'] == closest_value]
                )

                final.append(
                    {
                        "id": int(line_data['id'].values[0]),
                        "word": closest_value,
                        "theme": category,
                        "similarity": similarity
                    }
                )

        return final

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

        return ''.join([char for char in unicodedata.normalize('NFD', sentence)
                       if unicodedata.category(char) != 'Mn'])

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

    def find_closest_value(self, value_list, my_value):
        """ Find in a list the closest value to a given one.
        Parameters
        ----------
        my_value: string
            The subject value we want to match
        value_list: list
            The list of values where we iterate
        Returns
        ----------
        str
            The list closest value
        """
        prev_similarity = 10000  # Default Value - Never Remove

        for value in value_list:
            result = edlib.align(my_value, value)
            similarity = int(result["editDistance"])

            if similarity < prev_similarity:
                closest_value = value
                prev_similarity = similarity

            if similarity == 0:
                break

        return closest_value or ""
