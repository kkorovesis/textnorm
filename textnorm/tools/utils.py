# -*- coding: utf-8 -*-
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import os
import nltk
import datetime
import logging
from textnorm.tools.bad_words_list import get_bad_words_list
from textnorm.tools.slang_dict import slangdict

try:
  from nltk.corpus import brown
except Exception:
  nltk.download('brown')
  from nltk.corpus import brown
_HOMEFOLDER_ = os.environ['HOME']
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
logger = logging.getLogger()

STATS_DIR = _HOMEFOLDER_+'/corpora/ngram_stats/'
REGEX_TOKEN = re.compile(r'\b[a-z]{2,}\b')
NGRAM_SEP = "_"


def _unicode(text):
  try:
    text = unicode(text)
  except NameError:
    text = str(text)
  except Exception as e:
    print (e)
  return text


def unpack_contractions(text, expand_contractions):
  """
  Replace *English* contractions in ``text`` str with their unshortened forms.
  N.B. The "'d" and "'s" forms are ambiguous (had/would, is/has/possessive),
  so are left as-is.
  ---------
  ---------
  Important Note: The function is taken from textacy (https://github.com/chartbeat-labs/textacy).
  See textacy.preprocess.unpack_contractions(text)
  -> http://textacy.readthedocs.io/en/latest/api_reference.html#textacy.preprocess.unpack_contractions
  The reason that textacy is not added as a dependency is to avoid having the user to install it's dependencies (such as SpaCy),
  in order to just use this function.
  """

  d_contractions = {
    "can't've": "can't've",
    "couldn't've": "could not have",
    "hadn't've": "had not have",
    "he'd've": "he would have",
    "he'll've": "he will have",
    "how'd'y": "how do you",
    "I'd've": "I would have",
    "I'll've": "I will have",
    "it'd've": "it would have",
    "it'll've": "it will have",
    "mightn't've": "might not have",
    "mustn't've": "must not have",
    "needn't've": "need not have",
    "oughtn't've": "ought not have",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd've": "she would have",
    "she'll've": "she will have",
    "shouldn't've": "should not have",
    "that'd've": "that would have",
    "there'd've": "there would have",
    "they'd've": "they would have",
    "they'll've": "they will have",
    "we'd've": "we would have",
    "we'll've": "we will have",
    "what'll've": "what will have",
    "who'll've": "who will have",
    "won't've": "will not have",
    "wouldn't've": "would not have",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd've": "you would have",
    "you'll've": "you will have",
  }

  double_contractions_dict = {}
  for k, v in d_contractions.items():
    if not k in double_contractions_dict.keys():
      double_contractions_dict.update({k: [k, v]})

  if expand_contractions:

    for contr, ex_contr in double_contractions_dict.items():
      text = re.sub(contr, ex_contr[1], text)

    text = re.sub(
      r"(\b)([Aa]re|[Ww]as|[Aa]i|[Cc]ould|[Dd]id|[Dd]oes|[Dd]o|[Hh]ad|[Hh]as|[Hh]ave|[Ii]s|[Mm]ight|[Mm]ust|[Ss]hould|[Ww]ere|[Ww]ould|[Oo]ught|[Nn]eed|[Mm]ay)n't",
      r"\1\2 not", text)
    text = re.sub(
      r"(\b)([Hh]e|[Ii]|[Ss]he|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou|[Hh]ow)'ll",
      r"\1\2 will", text)
    text = re.sub(r"(\b)([Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou)'re", r"\1\2 are",
                  text)
    text = re.sub(
      r"(\b)([Ii]|[Cc]ould|[Ss]hould|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Ww]ould|[Yy]ou|[Ww]hy|)'ve",
      r"\1\2 have", text)
    # non-standard
    text = re.sub(r"(\b)([Aa]re)(?:'|’)n't", r"\1\2o not", text)
    text = re.sub(r"(\b)([Dd])(?:'|’)ya", r"\1\2o you all", text)
    text = re.sub(r"(\b)([Ii])(?:'|’)m", r"\1\2 am", text)
    text = re.sub(r"(\b)([Cc]a)n(?:'|’)t", r"\1\2n not", text)
    text = re.sub(r"(\b)([Ll]et)(?:'|’)s", r"\1\2 us", text)
    text = re.sub(r"(\b)([Ww])on(?:'|’)t", r"\1\2ill not", text)
    text = re.sub(r"(\b)([Ss])han(?:'|’)t", r"\1\2hall not", text)
    text = re.sub(r"(\b)([Ss])halln(?:'|’)t", r"\1\2hall not", text)
    text = re.sub(r"(\b)([Yy])(?:(?:'|’)all|a(?:'|’)ll)", r"\1\2ou all", text)

    text = re.sub(r"(\b)(([Ss]h|[Ww]her|[Tt]her|[Hh])e)(?:'|’)s", r"\1\2 is", text)
    text = re.sub(r"(\b)([Ss]o|[Hh]ow|[Ww]hy|[Ww]ho)(?:'|’)s", r"\1\2 is", text)
    text = re.sub(r"(\b)(([Ss]h|[Ww]her|[Tt]her|[Hh]|[Ww])e)(?:'|’)d", r"\1\2 would", text)
    text = re.sub(r"(\b)([Tt]hat|[Ii])(?:'|’)d", r"\1\2 would", text)

  else:

    for contr, ex_contr in double_contractions_dict.items():
      text = re.sub(contr, ex_contr[0], text)

    text = re.sub(r"(\b)([Dd])(?:'|’)ya", r"\1\2'ya", text)
    text = re.sub(r"(\b)([Ii])(?:'|’)m", r"\1\2'm", text)
    text = re.sub(r"(\b)([Cc]a)n(?:'|’)t", r"\1\2n't", text)
    text = re.sub(r"(\b)([Ll]et)(?:'|’)s", r"\1\2's", text)
    text = re.sub(r"(\b)([Ww])on(?:'|’)t", r"\1\2on't", text)
    text = re.sub(r"(\b)([Ss])han(?:'|’)t", r"\1\2hall't", text)
    text = re.sub(r"(\b)([Ss])halln(?:'|’)t", r"\1\2hall't", text)
    text = re.sub(r"(\b)([Yy])(?:(?:'|’)all|a(?:'|’)ll)", r"\1\2'all", text)

  return text


def handle_repeated_puncts(m):
  """
  return the sorted set so mathes random combinations of puncts
  will be mapped to the same token
  "!??!?!!", "?!!!!?!", "!!?", "!?!?" --> "?!"
  "!...", "...?!" --> ".!"
  :param m:
  :return:
  """
  text = m.group()
  text = "".join(sorted(set(text), reverse=True))

  return text


def dict_replace(wordlist, s_dict):
  """
  Replace token with token from dictionary
  :param wordlist:
  :param s_dict:
  :return:
  """

  return [s_dict[w] if w in s_dict else w for w in wordlist]


def remove_tags(doc):
  """
  Remove tags from sentence
  """
  doc = ' '.join(word for word in doc.split() if word[0] != '<[')
  return doc


def get_bad_words_dict():
  """
  Get Bad words dictionary {'word': '****'}
  :return:
  """

  bd_dict = {}
  for w in get_bad_words_list():
    bd_dict.update({
      w.lower(): '{0}'.format(''.join('*' for i in range(len(w)))),
      w.upper(): '{0}'.format(''.join('*' for i in range(len(w)))),
      w.capitalize(): '{0}'.format(''.join('*' for i in range(len(w))))
    })

  return bd_dict


def get_slang_dict():
  """
  Get dictionary with slang words and meaning
  :return:
  """

  # remove one char entries
  return {k: v for k, v in slangdict.items() if len(k.strip(" ")) > 1}




