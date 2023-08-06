# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['touca_fbs']

package_data = \
{'': ['*']}

install_requires = \
['flatbuffers>=23.1.4,<24.0.0']

setup_kwargs = {
    'name': 'touca-fbs',
    'version': '0.0.3',
    'description': 'Auto-generated python implementation of Touca FlatBuffers schema',
    'long_description': '# Touca FBS\n\nPackage with auto-generated Python implementation of Touca FlatBuffers schema\n',
    'author': 'Touca, Inc.',
    'author_email': 'hello@touca.io',
    'maintainer': 'Pejman Ghorbanzade',
    'maintainer_email': 'pejman@touca.io',
    'url': 'https://touca.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
