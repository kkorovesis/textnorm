#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re, os
from collections import Counter
import nltk
import datetime
try:
  from nltk.corpus import brown
except Exception:
  nltk.download('brown')
  from nltk.corpus import brown
import logging
import pickle
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
logger = logging.getLogger()


class SpellCorrector(object):
  """
  A spell corrector based on Peter Norvig's algorithm. Given a word or a text, returns the most probable
  correct word or word in text. NLTK brown corpus is used for dictionary. Future word:
    * Use more corpora
    * Provide text file for corpus
    * Use deep word matrix
    * Other techniques for optimum results
  """

  def __init__(self, **kwargs):
    self.corpus = kwargs.get('corpus', 'brown')
    self.pickled_words = kwargs.get('pickled_words', 'WORDS.pkl')
    self.WORDS = self.get_words()
    self.N = sum(self.WORDS.values())

  def get_words(self):
    """
    Word probabilities
    :param corpus:
    :param pickled_words:
    :return:
    """

    if os.path.exists(self.pickled_words):
      logger.info("Load language model for `{0}` corpus".format(self.corpus))
      words = pickle.load(open(self.pickled_words, 'rb'))
    else:
      logger.info("Creating WORDS dictionary for the first time. This might take a few minutes")
      text = ''
      if self.corpus == 'brown':
        for sent in brown.sents():
          text += " ".join(sent)
      words = re.findall(r'\w+', text.lower())
      pickle.dump(words, open(self.pickled_words, 'wb'))

    return Counter(words)

  def probability(self, word):
    """
    Probability of `word`.
    :param word:
    :param N:
    :return:
    """
    return float(self.WORDS[word] / self.N)

  @staticmethod
  def edit(word):
    """
    All edits that are one edit away from `word`. Peter Norvig's algorith
    :param word:
    :return:
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    candidates = set(deletes + transposes + replaces + inserts)
    return candidates

  def edits2(self, word):
    """
    All edits that are two edits away from `word`
    :param word:
    :return:
    """
    return (e2 for e1 in self.edit(word) for e2 in self.edit(e1))

  def edit_candidates(self, word, assume_wrong=False, fast=True):
    """
    Generate possible spelling corrections for word.
    :param word:
    :param assume_wrong:
    :param fast:
    :return:
    """
    if fast:
      if assume_wrong:
        return self.known(self.edit(word)) or [word]
      else:
        return self.known([word]) or self.known(self.edit(word)) or [word]
    else:
      if assume_wrong:
        ttt = self.known(self.edit(word)) or self.known(self.edits2(word)) or {word}
        return ttt
      else:
        return self.known([word]) or self.known(self.edit(word)) or self.known(self.edits2(word)) or [word]

  def known(self, words):
    """
    The subset of `words` that appear in the dictionary of WORDS.
    :param words: 
    :return: 
    """
    _ = set(w for w in words if w in self.WORDS)
    return _

  def correct(self, word, assume_wrong=False, fast=False):
    """
    Most probable spelling correction for word.
    :param word:
    :param assume_wrong:
    :param fast:
    :return:
    """
    return max(self.edit_candidates(word, assume_wrong=assume_wrong, fast=fast), key=self.probability)

  def correct_text(self, text):
    """
    Correct all the words within a text, returning the corrected text.
    :param text:
    :return:
    """
    return re.sub('[a-zA-Z]+', self.correct_match, text)

  def correct_match(self, m):
    """
    Spell-correct word in match, and preserve proper upper/lower/title case.
    :param m: match
    :return:
    """
    word = m.group()
    return self.case_of(word)(self.correct(word.lower()))

  @staticmethod
  def case_of(text):
    """
    Return the case-function appropriate for text: upper, lower, title, or just str.
    :param text:
    :return:
    """
    return str.upper if text.isupper() else str.lower if text.islower() else str.title if text.istitle() else str


def test():
  speller_params = {
    'corpus': 'brown',
  }
  sp = SpellCorrector(**speller_params)
  print("""
    Spell Corrector
    ================
    Word: {w:<3} => {cw:<3} 
    Text: {t:<3} => {ct:<3} 
    """.format(
      w='tecniques', cw=sp.correct('tecniques'),
      t='Iarth is not blat but a glofe', ct=sp.correct_text('Iarth is not blat but a glofe')
      )
  )


if __name__ == '__main__':
    test()




