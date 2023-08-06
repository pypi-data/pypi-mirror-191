# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trie_again', 'trie_again._ext']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trie-again',
    'version': '0.2.1',
    'description': 'Trie data structure for prefix search and text completion',
    'long_description': "# Trie Again: Python Trie implementation optimized for T9 completion\n\n\n## Installation\n\n```bash\n\npip install trie-again\n\n```\n\n## Usage\n\n```python\n\n# create an instance\nfrom trie_again import Trie\n\ntrie = Trie()\n\n# insert a single word\ntrie.insert('boy')\n\n# insert a list of words\ntrie.extend(['bondage', 'coverage'])\n\n# insert a list of words with multipliers (useful when parsing json)\ndata = {\n    'bondage': 10,\n    'coverage': 20,\n}\ntrie.extend(data.keys(), data.values())\n\n# check key in trie\nprint('bondage' in trie)\n# True\n\n# list all keys, sorted by usage\nprint(list(trie))\n# ['coverage', 'bondage', 'boy']\n\n# complete simple, sorted by usage\nprint(list(trie.complete('b')))\n# ['bondage', 'boy']\n```\n\n## T9 Like completion\n\n```python\n\n# complete with t9 like approach\nprint(list(trie.complete(['bc', 'o', 'vn'])))\n# ['coverage', 'bondage']\n\n```\n\n### How it works?\n\n```\n\nb o y\nb o n d a g e\nc o v e r a g e\n^ ^ ^\n1 2 3\n\n```\n\nWe use these groups to complete: `bc`, `o`, `vn`. It means that at position 1 it the letter may be `b` or `c`, at position 2 only `o`, at position 3 `v` or `n`.\n\n## Test\n\n```bash\n\n# test behavior\npoetry run pytest\n\n# test performance\npoetry run pytest --benchmark\n\n```\n\n## Dev\n\n```bash\n\n# very start\npoetry install\n\n# install pre commit\npoetry run pre-commit install\n\n# lint\npoetry run black .\npoetry run flake8 .\npoetry run mypy .\n\n# coverage\npoetry run coverage run -m pytest && poetry run coverage report -m\n\n# build package: limiting to sdist to compile it on install\npoetry build -f sdist\n```\n\n## Read an article about the trie, friends!\n\nhttps://blagovdaryu.hashnode.dev/ok-lets-trie-t9-in-python\n",
    'author': 'Egor Blagov',
    'author_email': 'e.m.blagov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
