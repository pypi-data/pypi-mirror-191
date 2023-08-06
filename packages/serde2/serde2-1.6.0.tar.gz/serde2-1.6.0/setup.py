# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serde']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=5.0.0,<6.0.0',
 'orjson>=3.8.2,<4.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'ujson>=5.5.0,<6.0.0']

extras_require = \
{':extra == "lz4" or extra == "all"': ['lz4>=4.0.2,<5.0.0']}

setup_kwargs = {
    'name': 'serde2',
    'version': '1.6.0',
    'description': 'Utilities for deserializing/serializing Python objects',
    'long_description': '# serde\nSet of utilities for deserializing/serializing Python objects\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/binh-vu/ream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
