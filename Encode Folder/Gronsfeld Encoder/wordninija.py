import gzip
import os
import re
from math import log


__version__ = '2.0.0'


# I did not author this code, only tweaked it from:
# http://stackoverflow.com/a/11642687/2449774
# Thanks Generic Human!


# Modifications by Scott Randal (Genesys)
#
# 1. Preserve original character case after splitting
# 2. Avoid splitting every post-digit character in a mixed string (e.g. 'win32intel')
# 3. Avoid splitting digit sequences
# 4. Handle input containing apostrophes (for possessives and contractions)
#
# Word list changes:
# Change 2 required adding single digits to the word list
# Change 4 required the following word list additions:
#   's
#   '
#   <list of contractions>
#  
# Dennis: For my project, I commented a few things out as I do allow
# punctuations in my enigma project.  



class LanguageModel(object):
    def __init__(self, word_file):
        # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
        with gzip.open(word_file) as f:
            words = f.read().decode().split()
        self._wordcost = dict((k, log((i+1)*log(len(words))))
                              for i, k in enumerate(words))
        self._maxword = max(len(x) for x in words)

    def split(self, s):
        """Uses dynamic programming to infer the location of spaces in a string without spaces."""
        punctuations = _SPLIT_RE.findall(s)
        texts = _SPLIT_RE.split(s)
        # assert len(punctuations) + 1 == len(texts)
        new_texts = [self._split(x) for x in texts]
        for i, punctuation in enumerate(punctuations):
            new_texts.insert(2*i+1, punctuation)
        return [item for sublist in new_texts for item in sublist]

    def _split(self, s):
        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        def best_match(i):
            candidates = enumerate(reversed(cost[max(0, i-self._maxword):i]))
            return min((c + self._wordcost.get(s[i-k-1:i].lower(), 9e999), k+1) for k, c in candidates)

        # Build the cost array.
        cost = [0]
        for i in range(1, len(s)+1):
            c, k = best_match(i)
            # if c > 100:
            #     c = 100
            # if c < 0:
            #     c = 1
            cost.append(int(c))

        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(s)
        while i > 0:
            c, k = best_match(i)
            # assert c == cost[i]
            # Apostrophe and digit handling (added by Genesys)
            newToken = True
            if not s[i-k:i] == "'":  # ignore a lone apostrophe
                if len(out) > 0:
                    # re-attach split 's and split digits
                    # digit followed by digit
                    if out[-1] == "'s" or (s[i-1].isdigit() and out[-1][0].isdigit()):
                        # combine current token with previous token
                        out[-1] = s[i-k:i] + out[-1]
                        newToken = False
            # (End of Genesys addition)

            if newToken:
                out.append(s[i-k:i])

            i -= k

        return reversed(out)


wordsPath = '/Users/dennis/Desktop/Break code/wordninja_words.txt.gz'
DEFAULT_LANGUAGE_MODEL = LanguageModel(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'wordninja_words.txt.gz'))
_SPLIT_RE = re.compile(r"\s+")


def split(s):
    return DEFAULT_LANGUAGE_MODEL.split(s)
