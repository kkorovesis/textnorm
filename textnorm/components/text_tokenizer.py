# -*- coding: utf-8 -*-
import sys
import re
import datetime
import logging
import traceback
from textnorm.components.regex_manager import RegexManager

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
dt = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
logger = logging.getLogger()
from textnorm.tools.handle_emoji import has_emoji, append_emojis_pattern

if sys.version_info[0] == 3:
  import html
  unescape = html.unescape
elif sys.version_info[0] == 2:
  import HTMLParser
  parser = HTMLParser.HTMLParser()
  unescape = lambda x: str(parser.unescape(x.decode('utf8')))

REGEX_PIPELINE = [
  "HTML_TAG", "URL", "DATE", "TIME", "PHONE", "CASHTAG", "PERCENT", "MONEY", "HASHTAG", "EMAIL", "USER", "QUOTES",
  "XNORM_TAG", "BBCODE", "PARENTHESIS", "BRACKET", "BRACES", "ACRONYM", "EMPHASIS", "CONTRACTION", "SPECIAL_CONTRACTION",
  "UNKNOWN_1", "LTR_FACE", "RTL_FACE", "REST_EMOTICONS", "EASTERN_EMOTICONS"
]


class Tokenizer(object):
  """
  TextNorm Tokenizer

  """

  def __init__(self, **kwargs):

    self.tokens = kwargs.get('tokens', False)
    self.regex_pipeline = kwargs.get('regex_pipeline', REGEX_PIPELINE)
    self.lowercase = kwargs.get('lowercase', False)
    self.special_dicts = kwargs.get('special_dicts', [])
    self.pickled_words = kwargs.get('pickled_words', None)

    self.pipeline = []
    self.regexes = RegexManager().expressions
    self.build_pipeline(self.regex_pipeline)
    all_patterns = "|".join(self.pipeline)  # join all patters to one GREEDY pattern for tokenization
    self.tok = re.compile(r"({})".format(all_patterns), flags=re.UNICODE | re.IGNORECASE)

  def build_pipeline(self, pipeline):
    for term in pipeline:
      self.pipeline.append(self.wrap_non_matching(self.regexes[(term)]))
    self.pipeline.append(self.wrap_non_matching(self.regexes['WORD']))

  @staticmethod
  def wrap_non_matching(exp):
    """
    Wrap expression in a Non-capturing group
    :param exp:
    :return:
    """

    return "(?:{})".format(exp)

  @staticmethod
  def dict_replace(wordlist, s_dict):
    """
    Repalce token with token from dictionary
    :param wordlist:
    :param s_dict:
    :return:
    """

    # todo: ignore case
    return [s_dict[w] if w in s_dict else w for w in wordlist]

  @staticmethod
  def join_tokens_in_text(tokens):
    """
    Joins tokens in texts
    :param tokens:
    :return:
    """

    text = ' '.join(tokens)
    text = re.sub(r"\b([\w_]+)\s(\/|-)\s([\w_]+)", r"\1\2\3", text)     # special cases
    text = re.sub(r"\b([\w_]+)\s([:])\s", r"\1\2 ", text)
    text = re.sub(r"\b([d])\s(['])\s(ya)", r"\1\2\3 ", text)
    return text

  def tokenize(self, text):
    """
    Tokenize text
    :param text:
    :param spell_corrector:
    :return:
    """

    if has_emoji(text):
      tokenized = self.tok.findall(text)
    else:
      escaped = unescape(text)  # remove special character quoting
      tokenized = self.tok.findall(escaped)

    if self.lowercase:
      tokenized = [t.lower() for t in tokenized]

    if self.special_dicts:
      for d in self.special_dicts:
        tokenized = self.dict_replace(tokenized, d)

    if not self.tokens:
      try:
        tokenized = self.join_tokens_in_text(tokenized)
      except TypeError as e:
        if 'tuple found' in str(e):
          logger.error("TypeError: sequence item 0: expected string, "
                       "tuple found, Maybe a regex is matches more than one group try using '?:' ")
          sys.exit(1)
        else:
          traceback.print_exc()
          sys.exit(1)

      for pm in ('\.','\?','\!','\,'):
        dot_space = re.compile(r'(\s(?:{0})(?:\s|$))'.format(pm))
        tokenized = re.sub(dot_space, '{0} ', tokenized).strip().format(pm).replace('\\', '')
      tokenized = re.sub(r' +', ' ', tokenized.strip())

    return tokenized


