# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from textnorm.patterns.expressions import EXPRESSIONS


class RegexManager(object):

  """
  Load regex dictionary and compile regexes
  """

  expressions = EXPRESSIONS

  def get_compiled(self):
    regexes = {k: re.compile(self.expressions[k], flags=re.UNICODE | re.IGNORECASE) for k, v in
               self.expressions.items()}
    return regexes
