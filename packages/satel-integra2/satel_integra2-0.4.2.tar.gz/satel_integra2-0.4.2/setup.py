# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['satel_integra2', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['cryptography']

extras_require = \
{':python_version >= "3.8" and python_version < "4.0"': ['click>=8.1.3,<9.0.0'],
 'dev': ['tox>=3.27.0,<4.0.0',
         'twine>=4.0.1,<5.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'test': ['pytest-cov>=4.0.0,<5.0.0',
          'pytest>=7.2.0,<8.0.0',
          'flake8>=5.0.4,<6.0.0']}

setup_kwargs = {
    'name': 'satel-integra2',
    'version': '0.4.2',
    'description': 'Communication library and basic testing tool for Satel Integra alarm system.',
    'long_description': '===============\nSatel Integra 2\n===============\n\n\n.. image:: https://img.shields.io/pypi/v/satel_integra2.svg\n        :target: https://pypi.python.org/pypi/satel_integra2\n\n.. image:: https://img.shields.io/pypi/pyversions/satel_integra2.svg\n        :target: https://pypi.org/project/satel_integra2/\n\n.. image:: https://readthedocs.org/projects/satel-integra2/badge/?version=latest\n        :target: https://satel-integra2.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n.. image:: https://github.com/wasilukm/satel_integra2/actions/workflows/dev.yml/badge.svg\n        :target: https://github.com/wasilukm/satel_integra2/actions/workflows/dev.yml\n\n.. image:: https://codecov.io/gh/wasilukm/satel_integra2/branch/main/graphs/badge.svg\n        :target: https://codecov.io/github/wasilukm/satel_integra2\n\nCommunication library and basic testing tool for Satel Integra alarm system. Communication via tcpip protocol published by SATEL.\n\nThis is a fork of https://github.com/c-soft/satel_integra.\n\n\n* Free software: MIT license\n* Documentation: https://satel-integra2.readthedocs.io.\n\n\nFeatures\n--------\n\n* all the features from the original `satel_integra` library in version 0.3.7\n* encrypted communication\n\nCredits\n---------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wasilukm/satel_integra2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
