# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['python_rule_engine']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'python-rule-engine',
    'version': '0.2.1',
    'description': 'A rule engine where rules are written in JSON format',
    'long_description': None,
    'author': 'Santiago Alvarez',
    'author_email': 'santiago.salvarez@mercadolibre.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/santalvarez/python-rule-engine',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
