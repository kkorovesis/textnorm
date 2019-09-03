# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import sys

is_narrow_unicode = sys.maxunicode < 0x10ffff
EMOJI_TAG = 'EMOJI'
NARROW_UNICODE_EMOJI = r"[\u2600-\u26FF\u2700-\u27BF]"
UNICODE_EMOJI=  r"[\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]"


def append_emojis_pattern(pipeline):

  if is_narrow_unicode:
    pipeline.insert(0, NARROW_UNICODE_EMOJI)
  else:
    pipeline.insert(0, UNICODE_EMOJI)
  return pipeline


def get_compiled():

  # todo: cashe RE_EMOJI

  if is_narrow_unicode:
    RE_EMOJI = re.compile(NARROW_UNICODE_EMOJI, flags=re.UNICODE | re.IGNORECASE)
  else:
    RE_EMOJI = re.compile(UNICODE_EMOJI, flags=re.UNICODE | re.IGNORECASE)
  return RE_EMOJI


def has_emoji(text):

  text = unicode(text)

  RE_EMOJI = get_compiled()
  if re.search(RE_EMOJI, text):
    return True
  else:
    return False


def tag_emoji(m, tag, mode):
  text = m.group()

  if mode == "single":
    return " {} <{}> ".format(text, tag)
  elif mode == "wrap":
    return " ".join([" <{}> {} </{}> ".format(tag, text, tag)]) + " "
  elif mode == "placeholder":
    return "<{}> ".format(tag)


def sub_emoji(text):

  text = unicode(text)
  RE_EMOJI = get_compiled()
  return RE_EMOJI.sub('<emoji>', text)


def add_special_emoji_tag(text, mode):

  text = unicode(text)
  RE_EMOJI = get_compiled()
  text = RE_EMOJI.sub(lambda w: tag_emoji(w, EMOJI_TAG, mode=mode), text)

  return text
