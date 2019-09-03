# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json

EXPRESSIONS = {

    "NARROW_UNICODE_EMOJI": r"[\u2600-\u26FF\u2700-\u27BF]",
    "UNICODE_EMOJI":  r"[\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]",
    "UNKNOWN_1": r'(?:\:\w{1,10}\:)',  # (:proud:, :cool:)
    "CONTRACTION": r'(?:\b\w+(?:)(?:\'|\’)(?:n|t|s|m|ve|d|ll|re|er|all|ya)\b(?:\'|\’)?(?:t|s|m|ve|d|ll|re|er|all|ya)?)',
    "SPECIAL_CONTRACTION": r'(?:\b(?:ma|o|)(?:\'|\’)(?:am|clock)|(?:\'cause))',
    "PARENTHESIS": r'\((?:.*?)\)',
    "BRACKET": r'\[(?:.*?)\]',
    "BRACES": r'\{(?:.*?)\}',
    "HASHTAG": r"\#\b[\w\-\_]+\b",
    "CASHTAG": r"(?<![A-Z])\$[A-Z]+\b",
    "TAG": r"<\[[\/]?\w+[\/]?\]>",
    "BBCODE": r'(?:\[)\w{1,10}(?:\])\S{2,}(?:\[)\/\w{1,10}(?:\])',
    "MATH": r'([-+]?[0-9]*\.?[0-9]+[\/\+\-\*])+([-+]?[0-9]*\.?[0-9]+)',
    "USER": r"\B\@\w+",
    "EMPHASIS": r"(?:\*\b\w+\b\*)",
    "CENSORED": r"(?:\b\w+\*+\w+\b)",
    "ACRONYM": r"\b(?:[A-Z]\.)(?:[A-Z]\.)+(?:\.(?!\.))?(?:[A-Z]\b)?",
    "QUOTES": r"\"(?:\\.|[^\"]){2,}\"",
    "REPEAT_PUNCTS": r"([!?.]){2,}",
    "REPEAT_CHARS": r"([-\|]){2,}",
    "EMAIL": r"(?:^|(?<=[^\w@.)]))(?:[\w+-](?:\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(?:\.(?:[a-z]{2,})){1,3}(?:$|(?=\b))",
    "PHONE": r"(?<![0-9])(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?![0-9])",
    "ALLCAPS": r"(?<![#@$])\b([A-Z][A-Z ]{1,}[A-Z])\b",
    "URL": r"(?:https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})",
    "LINKS": r"(?:https?\:\/\/|)(?:www.|)(?:)+(?:\w+\.)(?:com|gr|int|ru|edu|gov|net|org)\S*[\r\n\s\ ]*",
    "TIME": r"(?:(?:\d+)?\.?\d+(?:AM|PM|am|pm|a\.m\.|p\.m\.))|(?:(?:[0-2]?[0-9]|[2][0-3]):(?:[0-5][0-9])(?::(?:[0-5][0-9]))?(?: ?(?:AM|PM|am|pm|a\.m\.|p\.m\.))?)",
    "CAMEL_SPLIT": r"((?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])|[0-9]+|(?<=[0-9\-\_])[A-Za-z]|[\-\_])",
    "NORMALIZE_ELONG": r"(.)\1{2,}",
    "WORD": r"(?:[\w_]+)"
}