# simple_spell_checker

[![Coverage Status](https://img.shields.io/badge/%20Python%20Versions-%3E%3D3.9-informational)](https://pypi.org/project/simple-spell-checker/)
[![Coverage Status](https://coveralls.io/repos/github/SemioTricks/simple-spell-checker/badge.svg?branch=main)](https://coveralls.io/github/SemioTricks/simple-spell-checker?branch=main)

[![Coverage Status](https://img.shields.io/badge/Version-0.0.2-informational)](https://github.com/SemioTricks/simple-spell-checker)
[![Coverage Status](https://img.shields.io/badge/Docs-passed-green)](https://github.com/SemioTricks/simple-spell-checker/tree/main/simple_spell_checker_doc)


Simple Spell Checker is a spell checker based on prefix tree search. It find nearest to input word from known words (from input list). 
The algorithm finds mistakes in a word (insertions, deletions, replacements).

# Installation

> pip install simple-spell-checker

# Quickstart

```python
from simple_spell_checker.spell_checker import SpellChecker

cities = [
    "Kyiv", "Kharkiv", "Odesa", "Dnipro", "Donetsk", "Zaporizhzhia", "Lviv", 
    "Kryvyi Rih", "Mykolaiv", "Luhansk", "Vinnytsia", "Simferopol", "Chernihiv", 
    "Kherson", "Poltava", "Khmelnytskyi", "Cherkasy", "Chernivtsi", "Zhytomyr", "Sumy",
    "Rivne", "Ivano-Frankivsk", "Ternopil", "Kropyvnytskyi", "Lutsk", "Uzhhorod"
]

spell_checker = SpellChecker(max_corrections_relative=.5)
spell_checker.add_words(cities)

spell_checker.correction('Kiev')
# [{'word': 'Kyiv',
#   'corrections': [{'mistake_type': 'missing symbol "y"', 'position': 1},
#    {'mistake_type': 'extra symbol "e"', 'position': 2}]}]

spell_checker.correction('odessa')
# [{'word': 'Odesa',
#   'corrections': [{'mistake_type': 'wrong symbol "o": replaced on "O"',
#     'position': 0},
#    {'mistake_type': 'extra symbol "s"', 'position': 4}]}]

spell_checker.correction('Hmelnitskiy', max_corrections_relative=.5)
# [{'word': 'Khmelnytskyi',
#   'corrections': [{'mistake_type': 'missing symbol "K"', 'position': 0},
#    {'mistake_type': 'wrong symbol "H": replaced on "h"', 'position': 0},
#    {'mistake_type': 'wrong symbol "i": replaced on "y"', 'position': 5},
#    {'mistake_type': 'missing symbol "y"', 'position': 9},
#    {'mistake_type': 'extra symbol "y"', 'position': 10}]}]

spell_checker.correction('Kharkiv')
# [{'word': 'Kharkiv', 'corrections': []}]
```