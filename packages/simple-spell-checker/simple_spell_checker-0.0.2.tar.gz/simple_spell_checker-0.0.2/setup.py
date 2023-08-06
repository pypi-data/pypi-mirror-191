# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_spell_checker']

package_data = \
{'': ['*']}

install_requires = \
['fuzzy-multi-dict>=0.0.4,<0.0.5']

setup_kwargs = {
    'name': 'simple-spell-checker',
    'version': '0.0.2',
    'description': 'Simple Spell Checker is a spell checker based on prefix tree search. It find nearest to input word from known words (from input list). The algorithm finds mistakes in a word (insertions, deletions, replacements).',
    'long_description': '# simple_spell_checker\n\n[![Coverage Status](https://img.shields.io/badge/%20Python%20Versions-%3E%3D3.9-informational)](https://pypi.org/project/simple-spell-checker/)\n[![Coverage Status](https://coveralls.io/repos/github/SemioTricks/simple-spell-checker/badge.svg?branch=main)](https://coveralls.io/github/SemioTricks/simple-spell-checker?branch=main)\n\n[![Coverage Status](https://img.shields.io/badge/Version-0.0.2-informational)](https://github.com/SemioTricks/simple-spell-checker)\n[![Coverage Status](https://img.shields.io/badge/Docs-passed-green)](https://github.com/SemioTricks/simple-spell-checker/tree/main/simple_spell_checker_doc)\n\n\nSimple Spell Checker is a spell checker based on prefix tree search. It find nearest to input word from known words (from input list). \nThe algorithm finds mistakes in a word (insertions, deletions, replacements).\n\n# Installation\n\n> pip install simple-spell-checker\n\n# Quickstart\n\n```python\nfrom simple_spell_checker.spell_checker import SpellChecker\n\ncities = [\n    "Kyiv", "Kharkiv", "Odesa", "Dnipro", "Donetsk", "Zaporizhzhia", "Lviv", \n    "Kryvyi Rih", "Mykolaiv", "Luhansk", "Vinnytsia", "Simferopol", "Chernihiv", \n    "Kherson", "Poltava", "Khmelnytskyi", "Cherkasy", "Chernivtsi", "Zhytomyr", "Sumy",\n    "Rivne", "Ivano-Frankivsk", "Ternopil", "Kropyvnytskyi", "Lutsk", "Uzhhorod"\n]\n\nspell_checker = SpellChecker(max_corrections_relative=.5)\nspell_checker.add_words(cities)\n\nspell_checker.correction(\'Kiev\')\n# [{\'word\': \'Kyiv\',\n#   \'corrections\': [{\'mistake_type\': \'missing symbol "y"\', \'position\': 1},\n#    {\'mistake_type\': \'extra symbol "e"\', \'position\': 2}]}]\n\nspell_checker.correction(\'odessa\')\n# [{\'word\': \'Odesa\',\n#   \'corrections\': [{\'mistake_type\': \'wrong symbol "o": replaced on "O"\',\n#     \'position\': 0},\n#    {\'mistake_type\': \'extra symbol "s"\', \'position\': 4}]}]\n\nspell_checker.correction(\'Hmelnitskiy\', max_corrections_relative=.5)\n# [{\'word\': \'Khmelnytskyi\',\n#   \'corrections\': [{\'mistake_type\': \'missing symbol "K"\', \'position\': 0},\n#    {\'mistake_type\': \'wrong symbol "H": replaced on "h"\', \'position\': 0},\n#    {\'mistake_type\': \'wrong symbol "i": replaced on "y"\', \'position\': 5},\n#    {\'mistake_type\': \'missing symbol "y"\', \'position\': 9},\n#    {\'mistake_type\': \'extra symbol "y"\', \'position\': 10}]}]\n\nspell_checker.correction(\'Kharkiv\')\n# [{\'word\': \'Kharkiv\', \'corrections\': []}]\n```',
    'author': 'Tetiana Lytvynenko',
    'author_email': 'lytvynenkotv@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
