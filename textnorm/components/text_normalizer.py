# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import re
import os
import nltk
import datetime
import logging
# import unittest
from textnorm.components.text_tokenizer import Tokenizer
from textnorm.components.regex_manager import RegexManager
from textnorm.components.spell_correct import SpellCorrector
from textnorm.components.text_sanitizer import Sanitizer
from textnorm.tools.utils import unpack_contractions
from textnorm.tools.handle_emoji import add_special_emoji_tag

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
logger = logging.getLogger()


class TextNorm(object):

  """
  TextNorm (Text Normalizer) [docstring under construction]

  Kwargs:
    tokenizer: provide a tokenizer, we suggest using regex_tokenizer.Tokenizer
    sanitizer: provide a sanitizer, we suggest using regex_tokenizer.Sanitizer
    expand_contractions: set true to expand contractions (e.g. can't --> can not)
    tag_tokens: set true to tag every special token with the relative tag (e.g. 19-02-02 <DATE>)
    break_hashtags: set true to break hashtags (coming soon...)
    tag_mode: mode for tagging tokens (default: "wrap", <URL> https://regex101.com/ </URL> )
    segmenter_corpus: corpus from stats for text segmentation (use 'english')
    corrector_corpus: corpus for spell correction (e.g 'brown' for nltk.brown)

  """

  def __init__(self, **kwargs):
    self.tokenizer = kwargs.get('tokenizer', None)
    self.sanitizer = kwargs.get('sanitizer', None)
    self.speller = kwargs.get('speller', None)
    self.expand_contractions = kwargs.get('expand_contractions', False)
    self.tagging = kwargs.get('tagging', {})

    self.break_hashtags = kwargs.get('corrector_corpus', False)

    self.spell_corrector = None
    self.regexes = RegexManager().get_compiled()

  @staticmethod
  def add_tag(m, tag, mode):
    """
    Add tag to token
    :param m: match
    :param tag: tag (e.g. <URL>)
    :param mode: tag_mode
    :return:
    """

    text = m.group()
    if mode == "single":
      return " {} <[{}]> ".format(text, tag)
    elif mode == "wrap":
      return " ".join([" <[{}]> {} <[/{}]> ".format(tag, text, tag)]) + " "
    elif mode == "placeholder":
      return "<[{}]> ".format(tag)
    elif mode == "remove":
      return " "

    return text

  def preprocess(self, doc):
    """
    Pre-processing pipeline
    :param doc:
    :return:
    """

    # some pre-pre-processing
    doc = re.sub(r' +', ' ', doc.strip())

    doc = unpack_contractions(doc, self.expand_contractions)

    # sanitize text
    if doc and self.sanitizer:
      doc = self.sanitizer.text_filter(doc)

    # tagging
    for tag_mode in ['remove', 'placeholder', 'wrap', 'single']:
      tag_pipeline = self.tagging.get(tag_mode)
      for pattern in tag_pipeline:
        if pattern == "EMOJI":
          doc = add_special_emoji_tag(doc, mode=tag_mode)
        else:
          doc = self.regexes[pattern].sub(lambda w: self.add_tag(w, pattern, mode=tag_mode), doc)

    # tokenize text and match tokens
    if doc and self.tokenizer:
      doc = self.tokenizer.tokenize(doc, self.speller)

    else:
      return doc

    # todo: Replace tokens with special dictionaries (slang, emoticons ...)

    return doc

  def preprocess_docs(self, docs):
    """
    Generator for the pre-processing pipeline
    :param docs: list of docs
    :yield:
    """
    from tqdm import tqdm
    for d in tqdm(docs, desc="Normalizing Docs..."):
      yield self.preprocess(d)


# Replace bad words and slang
  from textnorm.tools.utils import get_bad_words_dict, get_slang_dict
  special_dicts = [
    get_bad_words_dict(),
    get_slang_dict(),
  ]



def test(data=None):

  logger.info("Run Test")

# Patters you want to tag

  handle_tags = {
    'single': [

    ],
    'wrap': [
      "URL", "PHONE", "DATE", "TIME", "CASHTAG", "PERCENT", "MONEY", "HASHTAG", "EMAIL", "USER",
      "BBCODE", "ACRONYM", "ASCI_ARROWS"
    ],
    'placeholder': [
      "EMOJI", "UNKNOWN_1", "LTR_FACE", "RTL_FACE", "REST_EMOTICONS", "EASTERN_EMOTICONS"
    ],
    'remove': [
      "HTML_TAG"
    ],
  }


# Replace bad words and slang
  from textnorm.tools.utils import get_bad_words_dict, get_slang_dict
  special_dicts = [
    get_bad_words_dict(),
    get_slang_dict(),
  ]

# Setup XNorm sanitizer
  sanitzer_params = {
    'merge_repeated_punc': True,
  }
  sanitizer = Sanitizer(**sanitzer_params)

# Setup XNorm Tokenizer
  tokenizer_params = {
    'tokens': False,
    'lowercase': True,
    'remove_stopwords': True,
    'special_dicts': special_dicts
  }
  tokenizer = Tokenizer(**tokenizer_params)

# # Setup XNorm Speller
# # WARNING: The first time is slow...
#   speller_params = {
#     'corpus': 'brown',
#   }
#   speller = SpellCorrector(**speller_params)

# Setup XNorm Normalizer
  textnorm_params = {
    # 'speller': speller,
    'sanitizer': sanitizer,
    'tokenizer': tokenizer,
    'expand_contractions': True,
    'tagging': handle_tags

  }
  x_normalizer = TextNorm(**textnorm_params)

  data = [
    "Let's here it for Spurs ＼(^o^)／!!! #coys #totenhamhotspurs. Aren't they amazing? :)))",
    "@SirajRaval:  can't wait for the Sep 12 #MachineLearning video!!! :-D https://www.youtube.com/channel/UCWN3xxRkmTPmbKwht9FuE5A",
    "Ited costs $2000 or $2K  and available at 10:26 AM, 2:15pm, 1:54 pm email me tmoz @ mpampisflou@yahoo.co.uk",
    "(o´▽`o) fuck C.I.A won't read this, I'm 99% sure:) 4gai <3",
    "<html><body> <a href='https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags?noredirect=1&amp;lq=1'>this question</a> </body></html>"
  ]

# Normalize document (text)
  x_normalizer.preprocess(data[0])

# Normalize many documents (less memory consuming)
  for doc_normd in x_normalizer.preprocess_docs(data):
    print(doc_normd)


if __name__ == '__main__':
  test()
