# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pocket_newsletter']

package_data = \
{'': ['*']}

install_requires = \
['pocket-api>=0.1.5,<0.2.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pocket_newsletter = pocket_newsletter.main:app']}

setup_kwargs = {
    'name': 'pocket-newsletter',
    'version': '0.1.3',
    'description': 'Retrieve articles from pocket',
    'long_description': '# Pocket Newsletter\n\nAllows extraction of articles in markdown set with newsletter tag from Pocket.\n',
    'author': 'José Cabeda',
    'author_email': 'jecabeda@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
