# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cashflow', 'cashflow.budget', 'cashflow.days', 'cashflow.statement']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0']

entry_points = \
{'console_scripts': ['budget_processor = cashflow.budget.cli:main',
                     'days_generator = cashflow.days.main:main',
                     'statement_processor = cashflow.statement.cli:main']}

setup_kwargs = {
    'name': 'cashflow-manager',
    'version': '0.5.0',
    'description': 'Import transaction in Notion cashflow and budget manager',
    'long_description': 'None',
    'author': 'lparolari',
    'author_email': 'luca.parolari23@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
