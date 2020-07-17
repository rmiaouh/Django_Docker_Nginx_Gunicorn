import sys
import json
import re
import string
import codecs
from collections import defaultdict
from symspellpy import SymSpell, Verbosity


class Model:
    rthographe_words = []
    sym_spell = None

    def __init__(self, language):
        # Initialize the model
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dictionary_path = "./{}_50k.txt".format(str(language))
        # term_index is the column of the term and count_index is the
        self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    def get_spellchecker_from_sentence(self, sentence):
        # Read the sentence
        input_term = str(sentence)

        # max edit distance per lookup (per single word)
        suggestions = self.sym_spell.lookup_compound(
            input_term, max_edit_distance=2, transfer_casing=True)
        # display suggestion term, edit distance, and term frequency
        for suggestion in suggestions:
            output_term = (str(suggestion)).split(",")[0]

        return output_term
