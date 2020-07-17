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
        import pathlib
        print(pathlib.Path(__file__).parent.absolute())
        print(pathlib.Path().absolute())
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dictionary_path = "./{}_50k.txt".format(str("fr"))
        f = open(dictionary_path, "r")
        print(f.read())
        self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    def get_spellchecker_from_sentence(self, sentence):

        input_term = str(sentence)

        suggestions = self.sym_spell.lookup_compound(
            input_term, max_edit_distance=2, transfer_casing=True)
        for suggestion in suggestions:
            output_term = (str(suggestion)).split(",")[0]

        return output_term
