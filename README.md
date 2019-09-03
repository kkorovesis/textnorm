#  XNorm (Generic Text Normalizer)

Python package for Text Normalizing

## Installation

```bash
pip install .
```
or directly:
```bash
pip install git+ssh://git@bitbucket.org/xplainlabs/xnorm.git
```

## Test

```python
from xnorm.components import text_normalizer
text_normalizer.test()

```

## Use

```python
from xnorm.components.text_normalizer import XNorm
from xnorm.components.text_sanitizer import Sanitizer
from xnorm.components.regex_tokenizer import Tokenizer

# Patters you want to tag
TAG_PATTERS = ["URL", "PHONE", "DATE", "TIME", "CASHTAG", "PERCENT", "MONEY", "HASHTAG", "EMAIL", "USER",
             "BBCODE", "ACRONYM", "EMOJI", "UNKNOWN_1", "LTR_FACE", "RTL_FACE", "REST_EMOTICONS", "EASTERN_EMOTICONS"]

# Replace bad words and slang
from xnorm.tools.utils import get_bad_words_dict, get_slang_dict
special_dicts = [
  get_bad_words_dict(),
  get_slang_dict(),
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
x_normalizer = XNorm(**xnorm_params)

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
```


## Scope

XNorm pipeline must include all necessary components to normalize user generated text in order to clean the text and
prepare it for analysis.


### Requirements

XNorm must take as input a document (text) or a list of documents and return the normalized text

XNorm main components:

* Text Normalizer
* UGC Tokenizer
* Spell Corrector
* Word Segmentation
* Text Sanitizer
* Regex Manager

Spell Corrector must:

* Create word probability dictionary from corpora
* Create probable world candidates
* Return most probable word

Word Segmentation must:

* Segmentate text to normal words

UGC Tokenizer must:

* Tokenize text be recognizing complex expressions or entities

Text Sanitizer must:

* Identify and pass on unwanted text patters
* Identify and pass on spamming text
* Extra cleaning on text (e.g. merge punctuations)

Regex Manager must:

* Load regexes

Text Normalizer must:

* preprocess text based on normalizer pipeline
* add tags in text (e.g. <[EMAIL]>, <[ACRONYM]>, <[EMOJI]>)



### Design

XNorm Spell Corrector is based on Peter Norvig's algorithm[1] for word editing. Tagging and Tokenizer
is based on ekphrasis[2]. Some features from textacy[3] are used in text pre-processing (only code snippets, no imports)

 [1] http://norvig.com/spell-correct.html

 [2] https://github.com/cbaziotis/ekphrasis

 [3] https://github.com/chartbeat-labs/textacy



Proposed steps:

1. Build GT main components separately
2. Create the normalizing pipeline
3. Build Unittests
4. Optimize each component
5. Add new features


### Testing

There must a text function for each component and a number of unittests

### Deployment
This packages requires the developing of 

* classes/objects:

    * Text Normalizer
    * UGC Tokenizer
    * Spell Corrector
    * Word Segmentation
    * Text Sanitizer
    * Regex Manager

* a library of functions

    * generate expressions
    * utilities
    * handle emojis


## Todo

### Need to have
 * [x] Spell Corrector
 * [x] Word Segmentation
 * [x] UGC Tokenizer
 * [x] Text Sanitizer
 * [x] Text normalization pipeline

### To do:
 * [x] Tag specials tokens
 * [x] Handle reapted panctuations
 * [x] Handle and tag unicode emojis
 * [x] Handle and tag more emoticons
 * [x] Generator for less memory consumption
 * [] Include Karakostas rules from cleanlib
 * [] Return "dirty" code from Sanitizer

### Future Work
 * [ ] Sophisticated spell correction
 * [ ] Recognizing expressions (emoticons)
 * [ ] Recognizing entities (dates, names, location)


## Structure 

    xnorm
    ├── README.md
    ├── setup.py
    └── xnorm
        ├── components
        │   ├── __init__.py
        │   ├── regex_manager.py
        │   ├── regex_tokenizer.py
        │   ├── spell_correct.py
        │   ├── text_normalizer.py
        │   ├── text_sanitizer.py
        │   ├── text_seg.py
        │   └── WORDS.pkl
        ├── __init__.py
        ├── regexes
        │   ├── generate_expressions.py
        │   └── __init__.py
        ├── tools
        │   ├── bad_words_list.py
        │   ├── handle_emoji.py
        │   ├── __init__.py
        │   ├── slang_dict.py
        │   └── utils.py
        └── utests.py


