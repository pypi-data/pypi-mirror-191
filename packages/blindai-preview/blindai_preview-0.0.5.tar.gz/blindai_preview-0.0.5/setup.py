# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blindai_preview']

package_data = \
{'': ['*']}

install_requires = \
['cbor2>=5.4.3,<6.0.0',
 'cryptography>=39.0.1,<40.0.0',
 'importlib-metadata>=6.0.0,<7.0.0',
 'numpy>=1.23.5,<1.24',
 'sgx-dcap-quote-verify-python>=0.0.3,<0.0.4',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'torch': ['torch>=1.13.0,<2.0.0']}

setup_kwargs = {
    'name': 'blindai-preview',
    'version': '0.0.5',
    'description': '',
    'long_description': '',
    'author': 'Corentin Lauverjat',
    'author_email': 'corentin.lauverjat@mithrilsecurity.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
