# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['advance_common']

package_data = \
{'': ['*']}

install_requires = \
['protobuf==3.19.4', 'pymavlink==2.4.27', 'pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'advance-common',
    'version': '1.1.6',
    'description': '',
    'long_description': '# Protobuf messages in messages_pb2 are tracked by git, so when importing this repo as submodule # there is no need to compile protobuf.\n\nIf you are reading this outside of PyPi, this project is published:\n```pip install advance-common```',
    'author': 'Szymon-SR',
    'author_email': 'srszymonsr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
