# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
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
    self.expand_contractions = kwargs.get('expand_contractions', False)
    self.tag_pipeline = kwargs.get('tag_pipeline', [])
    self.tag_tokens = kwargs.get('tag_tokens', True)
    self.segmenter_corpus = kwargs.get('segmenter_corpus', None)
    # self.corrector_corpus = kwargs.get('corrector_corpus', None)
    self.break_hashtags = kwargs.get('corrector_corpus', False)
    self.tag_mode = kwargs.get('tag_mode', 'wrap')

    self.segmenter = None
    self.regexes = RegexManager().get_compiled()
    # self.spell_corrector = None
    # if self.corrector_corpus:  # only brown corpus is available
    #   self.spell_corrector = SpellCorrector(corpus=self.corrector_corpus)

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

    # add special tag in text
    if doc and self.tag_tokens:
      for pattern in self.tag_pipeline:
        if pattern == "EMOJI":
          doc = add_special_emoji_tag(doc, mode=self.tag_mode)
        else:
          doc = self.regexes[pattern].sub(lambda w: self.add_tag(w, pattern, mode=self.tag_mode), doc)

    # tokenize text and match tokens
    if doc and self.tokenizer:
      doc = self.tokenizer.tokenize(doc)

    else:
      return doc

    # todo: test and add spell corrector
    # if doc and self.spell_corrector:
    #   doc = [self.spell_corrector.correct(t) for t in doc]

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
  TAG_PATTERS = ["URL", "PHONE", "DATE", "TIME", "CASHTAG", "PERCENT", "MONEY", "HASHTAG", "EMAIL", "USER",
                 "BBCODE", "ACRONYM", "EMOJI", "UNKNOWN_1", "LTR_FACE", "RTL_FACE", "REST_EMOTICONS", "EASTERN_EMOTICONS"]

  special_dicts = [
    {
      'fuck': '{0}'.format(''.join('*' for i in range(len('fuck'))))
    }
  ]

# Setup XNorm sanitizer
  sanitzer_params = {
    'min_text_length': 0,
    'max_digit_percentage': 0.85,
    'max_urls': 4,
    'merge_repeated_punc': True,
    'wc_ignore_patterns': TAG_PATTERS,
    'for_dataXS': False,
  }
  sanitizer = Sanitizer(**sanitzer_params)

# Setup XNorm Tokenizer
  tokenizer_params = {
    'tokens': False,
    'lowercase': False,
    'special_dicts': special_dicts
  }
  tokenizer = Tokenizer(**tokenizer_params)

# Setup XNorm Normalizer
  xnorm_params = {
    'tokenizer': tokenizer,
    'sanitizer': sanitizer,
    'expand_contractions': True,
    'tag_tokens': True,
    'tag_mode': 'wrap',
    'tag_pipeline': TAG_PATTERS,
  }
  x_normalizer = TextNorm(**xnorm_params)

  data = [
    "Let here it for Spurs ＼(^o^)／!!! #coys #totenhamhotspurs :)))",
    "@SirajRaval:  can't wait for the Sep 12 #MachineLearning video!!! :-D https://www.youtube.com/channel/UCWN3xxRkmTPmbKwht9FuE5A",
    "Item costs $2000 or $2K and available at 10:26 AM, 2:15pm, 1:54 pm email me @ mpampisflou@yahoo.co.uk",
    "(o´▽`o) fuck C.I.A won't read this, I'm 99% sure:) <3"
  ]

# Normalize document (text)
  x_normalizer.preprocess(data[0])

# Normalize many documents (less memory consuming)
  for doc_normd in x_normalizer.preprocess_docs(data):
    print(doc_normd)


if __name__ == '__main__':
  test()
