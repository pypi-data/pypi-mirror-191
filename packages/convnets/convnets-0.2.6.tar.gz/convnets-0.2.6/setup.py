# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convnets',
 'convnets.datasets',
 'convnets.models',
 'convnets.train',
 'convnets.train.imagenet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'convnets',
    'version': '0.2.6',
    'description': 'Convolutional Neural Networks and utilities for Computer Vision',
    'long_description': '# convnets\n\nConvolutional Neural Networks and utilities for Computer Vision.\n\n🚧 Under construction',
    'author': 'juansensio',
    'author_email': 'sensio.juan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
