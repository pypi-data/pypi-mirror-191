# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflow_ci', 'airflow_ci.api', 'airflow_ci.webhook']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.91.0,<0.92.0',
 'gitpython>=3.1.30,<4.0.0',
 'httpx>=0.23.3,<0.24.0',
 'orjson>=3.8.6,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'airflow-ci',
    'version': '0.0.3',
    'description': 'ci tool using airflow',
    'long_description': '[![Python package](https://github.com/phi-friday/airflow_ci/actions/workflows/lint.yml/badge.svg)](https://github.com/phi-friday/airflow_ci/actions/workflows/lint.yml)\n\nTODO:\n1. gitea implementation\n2. test code',
    'author': 'phi.friday',
    'author_email': 'phi.friday@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
