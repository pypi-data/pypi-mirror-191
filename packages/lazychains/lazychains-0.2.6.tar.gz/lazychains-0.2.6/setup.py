# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lazychains']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lazychains',
    'version': '0.2.6',
    'description': 'Singly linked lists with incremental instantiation of iterators',
    'long_description': '# Package Description\n\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/sfkleach/lazychains/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/sfkleach/lazychains/tree/main) [![Documentation Status](https://readthedocs.org/projects/lazychains/badge/?version=latest)](https://lazychains.readthedocs.io/en/latest/?badge=latest)\n\nA Python library to provide "chains", which are Lisp-like singly linked lists \nthat support the lazy expansion of iterators. For example, we can construct a \nChain of three characters from the iterable "abc" and it initially starts as \nunexpanded, shown by the three dots:\n\n```py\n>>> from lazychains import lazychain\n>>> c = lazychain( "abc")\n>>> c\nchain([...])\n```\n\nWe can force the expansion of *c* by performing (say) a lookup or by forcing the whole\nchain of items by calling expand:\n\n```py\n>>> c[1]                   # Force the expansion of the next 2 elements.\nTrue\n>>> c\nchain([\'a\',\'b\',...])\n>>> c.expand()             # Force the expansion of the whole chain.\nchain([\'a\',\'b\',\'c\'])\n```\n\nChain are typically a lot less efficient than using ordinary arrays. So,\nalmost all the time you should carry on using ordinary arrays and/or tuples.\nBut Chains have a couple of special features that makes them the \nperfect choice for some problems.\n\n   * Chains are immutable and hence can safely share their trailing segments.\n   * Chains can make it easy to work with extremely large (or infinite) \n     sequences.\n\nExpanded or Unexpanded\n----------------------\n\nWhen you construct a chain from an iterator, you can choose whether or not\nit should be immediately expanded by calling chain rather than lazychain.\nThe difference between the two is pictured below. First we can see what happens\nin the example given above where we create the chain using lazychain on \n"abc".\n\n![chain](https://user-images.githubusercontent.com/1164439/215340284-4b7b44a7-df32-4b90-b925-f0a395694805.png)\n\nBy contrast, we would immediately go to a fully expanded chain if we were to\nsimply apply chain:\n\n```py\n>>> from lazychains import chain\n>>> c = chain( "abc" )\n>>> c\nchain([\'a\',\'b\',\'c\'])\n>>> \n```\n\n![lazychain](https://user-images.githubusercontent.com/1164439/215340294-1667798e-dcad-402e-bccb-e0423f1e8ed9.png)\n\n',
    'author': 'Stephen Leach',
    'author_email': 'sfkleach@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lazychains.readthedocs.io/en/latest/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
