# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batframework']

package_data = \
{'': ['*'], 'batframework': ['data/*']}

install_requires = \
['pygame>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'batframework',
    'version': '0.1.0',
    'description': 'A pygame framework for making games easier',
    'long_description': '# Example Package\n\nPygame framework for making games easier.\n',
    'author': 'Baturay',
    'author_email': 'baturayturan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
