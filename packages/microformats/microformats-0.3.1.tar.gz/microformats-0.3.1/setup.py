# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mf', 'mf.parser', 'mf.parser.backcompat', 'mf.parser.prop_util']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'easyuri>=0.1.2',
 'html5lib>=1.1,<2.0',
 'requests>=2.28.2,<3.0.0',
 'txtint>=0.1.2']

entry_points = \
{'console_scripts': ['mf = mf:main']}

setup_kwargs = {
    'name': 'microformats',
    'version': '0.3.1',
    'description': 'tools for Microformats production, consumption and analysis',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/python-microformats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
