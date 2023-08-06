# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandus']

package_data = \
{'': ['*']}

install_requires = \
['pandas==1.5.3']

setup_kwargs = {
    'name': 'pandus',
    'version': '1.5.3.post2',
    'description': 'A simple wrapper around Pandas',
    'long_description': '# pandus\n[![PyPI version](https://badge.fury.io/py/pandus.svg)](https://badge.fury.io/py/pandus)\n\n## What is it?\n**pandus** is a fork of the popular data analysis library [pandas](https://pandas.pydata.org/), with the sole purpose of providing a different name. It provides a drop-in replacement for pandas, with all the same functionality and API, but with the name changed to "pandus".\n\nNote that while pandas is a serious library for data analysis, pandus is not intended to be taken seriously and is purely for fun. Use at your own risk!\n\n\n## Why?\nBecause of an inside joke.\n\n## Install\n```sh\npip install pandus\n```\n\n## Use\n```python3\nimport pandus as pd\n\n# just use it as you would use pandas\n```\n',
    'author': 'Egor Georgiev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/egor-georgiev/pandus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
