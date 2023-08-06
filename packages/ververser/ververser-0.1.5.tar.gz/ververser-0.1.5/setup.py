# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ververser',
 'ververser.examples.1_minimal',
 'ververser.examples.1_minimal.content',
 'ververser.examples.2_game_class',
 'ververser.examples.2_game_class.content']

package_data = \
{'': ['*']}

install_requires = \
['pyglet>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'ververser',
    'version': '0.1.5',
    'description': '',
    'long_description': 'None',
    'author': 'Berry',
    'author_email': 'berryvansomeren@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
