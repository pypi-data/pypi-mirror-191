# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eintf',
 'eintf.common',
 'eintf.db',
 'eintf.extractor',
 'eintf.extractor.map',
 'eintf.extractor.news']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'fastapi>=0.91.0,<0.92.0',
 'minify-html>=0.10.8,<0.11.0',
 'pymongo>=4.3.3,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'scrapy>=2.7.1,<3.0.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['eintf = eintf.main:run']}

setup_kwargs = {
    'name': 'eintf',
    'version': '0.0.5',
    'description': '',
    'long_description': 'Extractor for some tf2 websites [WIP]\n\n',
    'author': 'kshib',
    'author_email': 'ksyko@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
