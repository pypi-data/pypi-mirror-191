# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandus']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'pandus',
    'version': '1.5.3.2',
    'description': 'A simple wrapper around Pandas',
    'long_description': '# pandus: a wrapper around pandas, a powerful Python data analysis toolkit\n',
    'author': 'Egor Georgiev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
