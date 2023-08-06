# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supu']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0,<2.0', 'scipy>=1.9,<2.0']

setup_kwargs = {
    'name': 'supu',
    'version': '0.1.0',
    'description': 'Slightly Useful Python Utility functions',
    'long_description': '# SUPU\n\nSlightly Useful Python Utilities –\xa0a grab bag of small functions\n\nThese are really more like gists, but in a place where I can test them; if you want to\nuse them, it might just be easier to copy them into your own code than to add `supu` as\na dependency.\n',
    'author': 'Hugh Wimberly',
    'author_email': 'hugh.wimberly@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/moredatarequired/supu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
