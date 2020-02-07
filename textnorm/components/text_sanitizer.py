# -*- coding: utf-8 -*-
import re
import string
import datetime
import logging
from collections import Counter
from textnorm.components.regex_manager import RegexManager
from textnorm.tools.utils import handle_repeated_puncts

from nltk.tokenize.casual import _replace_html_entities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
logger = logging.getLogger()


class Sanitizer(object):

  """
  Designed to sanitize and filter out unwanted text.

  Kwargs:

  min_text_length: minimum text length allowed
  max_digit_percentage: maximum percentage for digits in text
  max_urls: maximum urls in text allowed
  wc_ignore_patterns: ignore patters when counting words (recommended: set equal to Tagged Patters)
  merge_repeated_punc: set true to merge repeated punctuations (e.g. goal!!! --> goal!)
  """

  def __init__(self, **kwargs):
    self.min_text_length = kwargs.get('min_text_length', 0)
    self.max_digit_percentage = kwargs.get('max_digit_percentage', 0.85)
    self.max_urls = kwargs.get('max_urls', 4)
    self.wc_ignore_patterns = kwargs.get('wc_ignore_patterns', ["URL", "HASHTAG"])
    self.merge_repeated_punc = kwargs.get('merge_repeated_punc', False)
    self.regexes = RegexManager().expressions
    self.compiled_regexes = RegexManager().get_compiled()

  def count_words(self, text):  # part of future version

    com_pat = re.compile(r"({})".format("|".join(self.regexes[pat] for pat in self.wc_ignore_patterns)))
    text = re.sub(com_pat, '', text)

    rm_punct = re.compile('[%s]' % re.escape(string.punctuation))
    text = re.sub(rm_punct, '', text)

    word_cound = len(re.split(r'\s', text.strip()))
    return word_cound

  def count_occurrences(self, text, pattern):  # part of future version

    com_pat = re.compile(self.regexes[pattern])
    return len(com_pat.findall(text))

  @staticmethod
  def num_most_freq_chars(text, num_top):  # part of future version
    c = Counter(text)
    for key in list(c.elements()):
      if key in '0123456789*#@$=+-_':
        del c[key]
    return c.most_common(num_top)

  @staticmethod
  def num_most_freq_words(text, num_top):  # part of future version
    cnt = Counter()
    exclude_words = ['and', 'the', 'of']
    for w in re.split('\s', text):
      if w != '' and w not in exclude_words and len(w) > 3:
        cnt[w] += 1
    return cnt.most_common(num_top)

  @staticmethod
  def num_digits_per_words(text):  # part of future version
    digits = 0
    non_digits = 1
    for iW in re.split(r'\s', text):
      if iW not in string.punctuation:
        for i in iW:
          if i.isdigit():
            digits += 1
          else:
            non_digits += 1
    return 1. * digits / non_digits

  def text_filter(self, text):

    text = text.replace('|||', ' ')
    text = _replace_html_entities(text)

    if text and self.merge_repeated_punc:
      text = self.compiled_regexes["REPEAT_PUNCTS"].sub(
        lambda w: handle_repeated_puncts(w), text)

    text = self.compiled_regexes["REPEAT_CHARS"].sub(
      lambda w: handle_repeated_puncts(w), text)

    return text



