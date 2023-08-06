# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lcdp_postgres_utils',
 'lcdp_postgres_utils.executors',
 'lcdp_postgres_utils.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.55,<2.0.0', 'pg8000>=1.29.4,<2.0.0']

setup_kwargs = {
    'name': 'lcdp-postgres-utils',
    'version': '1.0.4.dev35',
    'description': 'Postgres Utils to create users, databases, functions, ...',
    'long_description': 'None',
    'author': 'Le Comptoir Des Pharmacies',
    'author_email': 'webmaster@lecomptoirdespharmacies.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
