# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['binobj', 'binobj.fields']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=4.0']

extras_require = \
{':python_version < "3.8"': ['typing-inspect>=0.4.0']}

setup_kwargs = {
    'name': 'binobj',
    'version': '0.11.0',
    'description': 'A Python library for reading and writing structured binary data.',
    'long_description': 'None',
    'author': 'Diego Argueta',
    'author_email': '620513-dargueta@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
