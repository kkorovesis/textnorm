#  TextNorm (Text Normalizer)

Python package for Text Normalizing. The purpose of this project is to build a standalone text normalizer for text pre-processing. Version 0.3 includes:

* Spell correct: Correct spelling based in Peter Norvig's algorithm.

* Text sanitization: Merge repeated punctuation or characters, handle contractions

* Text tagging: Place tag on patterns (URL, USER, ACRONYM, EMOJIS among other)

* Text tokenization: Tokenize text (match known patterns)


## Installation

```bash
git clone https://github.com/kkorovesis/textnorm
cd textnorm
pip install .

## Test

```python
from textnorm.components import text_normalizer
text_normalizer.test()
```


TextNorm Spell Corrector is based on Peter Norvig's algorithm[1] for word editing. Tagging and Tokenizer
is based on ekphrasis[2]. Some features from textacy[3] are used in text pre-processing (only code snippets, no imports)

 [1] http://norvig.com/spell-correct.html

 [2] https://github.com/cbaziotis/ekphrasis

 [3] https://github.com/chartbeat-labs/textacy

## Structure

    textnorm/
    ├── README.md
    ├── setup.py
    └── textnorm
        ├── components
        │   ├── __init__.py
        │   ├── regex_manager.py
        │   ├── text_normalizer.py
        │   ├── text_sanitizer.py
        │   └── text_tokenizer.py
        ├── __init__.py
        ├── patterns
        │   ├── expressions.py
        │   └── __init__.py
        └── tools
            ├── bad_words_list.py
            ├── handle_emoji.py
            ├── __init__.py
            ├── slang_dict.py
            └── utils.py

