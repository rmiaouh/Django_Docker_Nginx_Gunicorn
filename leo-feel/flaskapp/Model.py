import math, re, sys, fnmatch, string, codecs, unicodedata
import pandas as pd

class Model:
    word_valence_dict = {}
    boosters = {}
    negations = {}
    punctuations = [
        ".",
        "!",
        "?",
        ",",
        ";",
        ":",
        "-",
        "'",
        "\"",
        "!!",
        "!!!",
        "??",
        "???",
        "?!?",
        "!?!",
        "?!?!",
        "!?!?"
    ]


    def __init__(self, language):
        # Import lexic
        lexic_df = pd.read_csv("./assets/words_rating.csv", delimiter=",", names=["word", "note"])
        for _, row in lexic_df.iterrows():
            self.word_valence_dict[row["word"]] = float(row["note"])

        # Import boosters
        boosters_df = pd.read_csv("./assets/boosters.csv", delimiter=",", names=["word", "incrementation"])
        for _, row in boosters_df.iterrows():
            self.boosters[row["word"]] = float(row["incrementation"])

        # Import negations
        with codecs.open("./assets/negations.txt", encoding='utf8') as f:
            negations_data = f.read()

        self.negations = negations_data.split('\n')


    def strip_accents_str(self, sentence):
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

        return ''.join(c for c in unicodedata.normalize('NFD', str(sentence))
                if unicodedata.category(c) != 'Mn')


    def check_negation(self, sentence_words, negation_words=[], includeNT=True):
        """
            Check if a list of words contain negations
            Parameters
            ----------
            sentence_words : list
                List of words present in the sentence
            negation_words : list
                List of negative words to complement the existing list
            includeNT : boolean
                Don't know
            Returns
            -------
            boolean
                Negation presence in the list
        """

        negation_words.extend(self.negations)

        for word in negation_words:
            if word in sentence_words:
                return True

        if includeNT: # @TODO: change this code to work with all languages
            for word in sentence_words:
                if "n'a" in word:
                    return True

        if "least" in sentence_words: # @TODO: change this code to work for all languages
            i = sentence_words.index("least")
            if i > 0 and sentence_words[i-1] != "at":
                return True

        return False


    def get_feelings_from_sentence(self, text):
        text = self.strip_accents_str(text)
        wordsAndEmoticons = str(text).split() #doesn't separate words from adjacent punctuation (keeps emoticons & contractions)

        # removes punctuation (but loses emoticons & contractions)
        regex_remove_punctuation = re.compile('[%s]' % re.escape(string.punctuation))
        text_mod = regex_remove_punctuation.sub('', text)

        # get rid of empty items or single letter "words" like 'a' and 'I' from wordsOnly
        wordsOnly = str(text_mod).split()
        for word in wordsOnly:
            if len(word) <= 1:
                wordsOnly.remove(word)

        # now remove adjacent & redundant punctuation from [wordsAndEmoticons] while keeping emoticons and contractions
        for word in wordsOnly:
            for p in self.punctuations:
                pword = p + word
                x1 = wordsAndEmoticons.count(pword)
                while x1 > 0:
                    i = wordsAndEmoticons.index(pword)
                    wordsAndEmoticons.remove(pword)
                    wordsAndEmoticons.insert(i, word)
                    x1 = wordsAndEmoticons.count(pword)

                wordp = word + p
                x2 = wordsAndEmoticons.count(wordp)
                while x2 > 0:
                    i = wordsAndEmoticons.index(wordp)
                    wordsAndEmoticons.remove(wordp)
                    wordsAndEmoticons.insert(i, word)
                    x2 = wordsAndEmoticons.count(wordp)

        # get rid of residual empty items or single letter "words" like 'a' and 'I' from wordsAndEmoticons
        for word in wordsAndEmoticons:
            if len(word) <= 1:
                wordsAndEmoticons.remove(word)

        # remove stopwords from [wordsAndEmoticons]
        #if we want to add stopwords put it here

        def normalize(score, alpha=15):
            # normalize the score to be between -1 and 1 using an alpha that approximates the max expected value
            normScore = score/math.sqrt( ((score*score) + alpha) )
            return normScore

        def wildCardMatch(patternWithWildcard, listOfStringsToMatchAgainst): #@TODO: Can I delete this ? It is not used anywhere
            listOfMatches = fnmatch.filter(listOfStringsToMatchAgainst, patternWithWildcard)
            return listOfMatches

        def isALLCAP_differential(wordList):
            countALLCAPS= 0
            for w in wordList:
                if str(w).isupper():
                    countALLCAPS += 1
            cap_differential = len(wordList) - countALLCAPS
            if cap_differential > 0 and cap_differential < len(wordList):
                isDiff = True
            else: isDiff = False
            return isDiff
        isCap_diff = isALLCAP_differential(wordsAndEmoticons)

        sentiments = []
        for item in wordsAndEmoticons:
            v = 0
            i = wordsAndEmoticons.index(item)

            if (i < len(wordsAndEmoticons)-1 and str(item).lower() == "un peu" and \
            str(wordsAndEmoticons[i+1]).lower() == "de") or str(item).lower() in self.boosters: # @TODO: change this code to work with all languages
                sentiments.append(v)
                continue
            item_lowercase = str(item).lower()
            if  item_lowercase in self.word_valence_dict:
                #get the sentiment valence
                v = float(self.word_valence_dict[item_lowercase])

                #check if sentiment laden word is in ALLCAPS (while others aren't)
                c_incr = 0.733 #(empirically derived mean sentiment intensity rating increase for using ALLCAPs to emphasize a word)
                if str(item).isupper() and isCap_diff:
                    if v > 0: v += c_incr
                    else: v -= c_incr

                #check if the preceding words increase, decrease, or negate/nullify the valence
                def scalar_inc_dec(word, valence):
                    scalar = 0.0
                    word_lower = str(word).lower()
                    if word_lower in self.boosters:
                        scalar = self.boosters[word_lower]
                        if valence < 0: scalar *= -1
                        #check if booster/dampener word is in ALLCAPS (while others aren't)
                        if str(word).isupper() and isCap_diff:
                            if valence > 0: scalar += c_incr
                            else:  scalar -= c_incr
                    return scalar
                n_scalar = -0.74

                if i > 0 and str(wordsAndEmoticons[i-1]).lower() not in self.word_valence_dict:
                    s1 = scalar_inc_dec(wordsAndEmoticons[i-1], v)
                    v = v+s1
                    if self.check_negation([wordsAndEmoticons[i-1]]):
                        v = v*n_scalar
                        if v > 0 :
                            v = -1.0
                if i > 1 and str(wordsAndEmoticons[i-2]).lower() not in self.word_valence_dict:
                    s2 = scalar_inc_dec(wordsAndEmoticons[i-2], v)
                    if s2 != 0: s2 = s2*0.95
                    v = v+s2
                    # check for special use of 'never' as valence modifier instead of negation
                    if wordsAndEmoticons[i-2] == "jamais" and (wordsAndEmoticons[i-1] == "jamais"): # @TODO: change this code to work with all languages
                        v = v*1.5
                    # otherwise, check for negation/nullification
                    elif self.check_negation([wordsAndEmoticons[i-2]]):
                        v = v*n_scalar
                        if v > 0 :
                            v = -1.0
                if i > 2 and str(wordsAndEmoticons[i-3]).lower() not in self.word_valence_dict:
                    s3 = scalar_inc_dec(wordsAndEmoticons[i-3], v)
                    if s3 != 0: s3 = s3*0.9
                    v = v+s3
                    # check for special use of 'never' as valence modifier instead of negation
                    if wordsAndEmoticons[i-3] == "jamais" and \
                    (wordsAndEmoticons[i-2] == "de" or wordsAndEmoticons[i-2] == "ca") or \
                    (wordsAndEmoticons[i-1] == "de" or wordsAndEmoticons[i-1] == "ca"): # @TODO: change this code to work with all languages
                        v = v*1.25
                    # otherwise, check for negation/nullification
                    elif self.check_negation([wordsAndEmoticons[i-3]]):
                        v = v*n_scalar
                        if v > 0 :
                            v = -1.0

                    # check for special case idioms using a sentiment-laden keyword known to SAGE
                    special_case_idioms = {"pas de probleme": 3, "the bomb": 3, "bad ass": 1.5, "yeah right": -2,
                                        "cut the mustard": 2, "kiss of death": -1.5, "hand to mouth": -2} # @TODO: change this code to work with all languages
                    # future work: consider other sentiment-laden idioms
                    #other_idioms = {"back handed": -2, "blow smoke": -2, "blowing smoke": -2, "upper hand": 1, "break a leg": 2,
                    #                "cooking with gas": 2, "in the black": 2, "in the red": -2, "on the ball": 2,"under the weather": -2}
                    onezero = "{} {}".format(str(wordsAndEmoticons[i-1]), str(wordsAndEmoticons[i]))
                    twoonezero = "{} {} {}".format(str(wordsAndEmoticons[i-2]), str(wordsAndEmoticons[i-1]), str(wordsAndEmoticons[i]))
                    twoone = "{} {}".format(str(wordsAndEmoticons[i-2]), str(wordsAndEmoticons[i-1]))
                    threetwoone = "{} {} {}".format(str(wordsAndEmoticons[i-3]), str(wordsAndEmoticons[i-2]), str(wordsAndEmoticons[i-1]))
                    threetwo = "{} {}".format(str(wordsAndEmoticons[i-3]), str(wordsAndEmoticons[i-2]))
                    if onezero in special_case_idioms: v = special_case_idioms[onezero]
                    elif twoonezero in special_case_idioms: v = special_case_idioms[twoonezero]
                    elif twoone in special_case_idioms: v = special_case_idioms[twoone]
                    elif threetwoone in special_case_idioms: v = special_case_idioms[threetwoone]
                    elif threetwo in special_case_idioms: v = special_case_idioms[threetwo]
                    if len(wordsAndEmoticons) - 1 > i:
                        zeroone = "{} {}".format(str(wordsAndEmoticons[i]), str(wordsAndEmoticons[i+1]))
                        if zeroone in special_case_idioms: v = special_case_idioms[zeroone]
                    if len(wordsAndEmoticons) - 1 > i + 1:
                        zeroonetwo = "{} {} {}".format(str(wordsAndEmoticons[i]), str(wordsAndEmoticons[i+1]), str(wordsAndEmoticons[i+2]))
                        if zeroonetwo in special_case_idioms: v = special_case_idioms[zeroonetwo]

                    # check for booster/dampener bi-grams such as 'sort of' or 'kind of'
                    if threetwo in self.boosters or twoone in self.boosters:
                        v -= 0.293

                # check for negation case using "least"
                if i > 1 and str(wordsAndEmoticons[i-1]).lower() not in self.word_valence_dict \
                    and str(wordsAndEmoticons[i-1]).lower() == "least": # @TODO: change this code to work with all languages
                    if (str(wordsAndEmoticons[i-2]).lower() != "at" and str(wordsAndEmoticons[i-2]).lower() != "very"): # @TODO: change this code to work with all languages
                        v = v*n_scalar
                elif i > 0 and str(wordsAndEmoticons[i-1]).lower() not in self.word_valence_dict \
                    and str(wordsAndEmoticons[i-1]).lower() == "least": # @TODO: change this code to work with all languages
                    v = v*n_scalar
            sentiments.append(v)

        # check for modification in sentiment due to contrastive conjunction 'but'
        if 'mais' in wordsAndEmoticons or 'MAIS' in wordsAndEmoticons: # @TODO: change this code to work with all languages
            try: bi = wordsAndEmoticons.index('mais') # @TODO: change this code to work with all languages
            except: bi = wordsAndEmoticons.index('MAIS') # @TODO: change this code to work with all languages
            for s in sentiments:
                si = sentiments.index(s)
                if si < bi:
                    sentiments.pop(si)
                    sentiments.insert(si, s*0.2)
                elif si > bi:
                    sentiments.pop(si)
                    sentiments.insert(si, s*1.2)

        if sentiments:
            sum_s = float(sum(sentiments))
            #print sentiments, sum_s

            # check for added emphasis resulting from exclamation points (up to 4 of them)
            ep_count = str(text).count("!")
            if ep_count > 4: ep_count = 4
            ep_amplifier = ep_count*0.292 #(empirically derived mean sentiment intensity rating increase for exclamation points)
            if sum_s > 0:  sum_s += ep_amplifier
            elif  sum_s < 0: sum_s -= ep_amplifier

            # check for added emphasis resulting from question marks (2 or 3+)
            qm_count = str(text).count("?")
            qm_amplifier = 0
            if qm_count > 1:
                if qm_count <= 3: qm_amplifier = qm_count*0.18
                else: qm_amplifier = 0.96
                if sum_s > 0:  sum_s += qm_amplifier
                elif  sum_s < 0: sum_s -= qm_amplifier

            compound = normalize(sum_s)

            # want separate positive versus negative sentiment scores
            pos_sum = 0.0
            neg_sum = 0.0
            neu_count = 0
            for sentiment_score in sentiments:
                if sentiment_score > 0:
                    pos_sum += (float(sentiment_score) +1) # compensates for neutral words that are counted as 1
                if sentiment_score < 0:
                    neg_sum += (float(sentiment_score) -1) # when used with math.fabs(), compensates for neutrals
                if sentiment_score == 0:
                    neu_count += 1

            if pos_sum > math.fabs(neg_sum): pos_sum += (ep_amplifier+qm_amplifier)
            elif pos_sum < math.fabs(neg_sum): neg_sum -= (ep_amplifier+qm_amplifier)

            total = pos_sum + math.fabs(neg_sum) + neu_count
            pos = math.fabs(pos_sum / total)
            neg = math.fabs(neg_sum / total)
            neu = math.fabs(neu_count / total)

        else:
            compound = 0.0; pos = 0.0; neg = 0.0; neu = 0.0

        return {
            "negative" : round(neg, 3),
            "neutral" : round(neu, 3),
            "positive" : round(pos, 3),
            "compound" : round(compound, 4)
        }
