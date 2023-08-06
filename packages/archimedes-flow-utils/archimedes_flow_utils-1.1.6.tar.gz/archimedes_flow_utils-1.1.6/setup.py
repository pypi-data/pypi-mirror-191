# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['archimedes_flow_utils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'azure-core>=1.23.1,<2.0.0',
 'azure-storage-blob>=12.11.0,<13.0.0',
 'prefect>=1.2.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'archimedes-flow-utils',
    'version': '1.1.6',
    'description': 'Common code for all our prefect flows',
    'long_description': 'None',
    'author': 'Optimeering AS',
    'author_email': 'dev@optimeering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
