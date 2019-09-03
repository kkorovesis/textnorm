#  TextNorm (Text Normalizer)

Python package for Text Normalizing

## Installation

```bash
git clone https://github.com/kkorovesis/textnorm
cd textnorm
pip install .

```
or directly:
```bash
pip install git+ssh://git@github.com/kkorovesis/textnorm
```

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

