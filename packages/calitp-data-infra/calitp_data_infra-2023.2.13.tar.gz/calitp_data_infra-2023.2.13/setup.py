# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calitp_data_infra']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2.1,<3.0.0',
 'calitp-data==2023.2.13',
 'google-api-core>=1.32.0,<2.0.0dev',
 'google-cloud-bigquery-storage==2.14.1',
 'humanize>=4.6.0,<5.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.9,<1.10',
 'tqdm>=4.64.1,<5.0.0',
 'typing-extensions>=3.10.0.2']

setup_kwargs = {
    'name': 'calitp-data-infra',
    'version': '2023.2.13',
    'description': '',
    'long_description': 'None',
    'author': 'Andrew Vaccaro',
    'author_email': 'andrew.v@jarv.us',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
