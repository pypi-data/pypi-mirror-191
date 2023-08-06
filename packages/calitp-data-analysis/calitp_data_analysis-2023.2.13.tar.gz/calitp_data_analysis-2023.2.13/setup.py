# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calitp_data_analysis']

package_data = \
{'': ['*']}

install_requires = \
['calitp-data==2023.2.13',
 'ipython>=8.9.0,<9.0.0',
 'jinja2<3.1.0',
 'pandas-gbq>=0.19.1,<0.20.0',
 'siuba>=0.4.2,<0.5.0',
 'sqlalchemy-bigquery>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'calitp-data-analysis',
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
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
