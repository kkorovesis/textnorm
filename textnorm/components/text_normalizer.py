# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import re
import os
import nltk
import datetime
import logging
# import unittest
from text_tokenizer import Tokenizer
from regex_manager import RegexManager
from xnorm.tools.utils import unpack_contractions
from xnorm.tools.handle_emoji import add_special_emoji_tag

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
    self.expand_contractions = kwargs.get('expand_contractions', False)
    self.tag_pipeline = kwargs.get('tag_pipeline', [])
    self.tag_tokens = kwargs.get('tag_tokens', True)
    self.tag_mode = kwargs.get('tag_mode', 'wrap')

    self.segmenter = None
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

    # todo: include text cleaning

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


def test():

  logger.info("Run Test")

# Patters you want to tag
  TAG_PATTERS = ["URL"]

  # todo: add repl_dicts

  # todo: add text cleaner

# Setup XNorm Tokenizer
  tokenizer_params = {
    'tokens': False,
  }
  tokenizer = Tokenizer(**tokenizer_params)

# Setup XNorm Normalizer
  xnorm_params = {
    'tokenizer': tokenizer,
    'expand_contractions': True,
    'tag_tokens': True,
    'tag_mode': 'placeholder',
    'tag_pipeline': TAG_PATTERS,
  }
  x_normalizer = TextNorm(**xnorm_params)

  data = [
    "Let here it for Spurs ＼(^o^)／!!! #coys #totenhamhotspurs :)))",
    "@SirajRaval:  can't wait for the Sep 12 #MachineLearning video!!! :-D https://www.youtube.com/channel/UCWN3xxRkmTPmbKwht9FuE5A",
    "Item costs $2000 or $2K and available at 10:26 AM, 2:15pm, 1:54 pm email me tmoz @ mpampisflou@yahoo.co.uk",
    "(o´▽`o) fuck C.I.A won't read this, I'm 99% sure:) 4gai <3"
  ]

# Normalize document (text)
  x_normalizer.preprocess(data[0])

# Normalize many documents (less memory consuming)
  for doc_normd in x_normalizer.preprocess_docs(data):
    print(doc_normd)


if __name__ == '__main__':
  test()
