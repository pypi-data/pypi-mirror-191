# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyc3']

package_data = \
{'': ['*'], 'pyc3': ['data/xkcd/c3_data.json']}

install_requires = \
['colorutil>=0.9.1,<0.10.0', 'numpy>=1.21.6,<2.0.0']

setup_kwargs = {
    'name': 'pyc3',
    'version': '0.3.1',
    'description': '',
    'long_description': "Python implementation of Jeff Heer's C3 color naming model,\noutlined in\n\n```bibtex\nJeffrey Heer and Maureen Stone. 2012. \nColor naming models for color selection, image editing and palette design. \nIn Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '12). \nAssociation for Computing Machinery, New York, NY, USA, 1007â\x80\x931016. \nhttps://doi-org.ezp-prod1.hul.harvard.edu/10.1145/2207676.2208547\n```\n\n",
    'author': 'Simon Warchol',
    'author_email': 'simonwarchol@g.harvard.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonwarchol/pyc3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
