# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sa_repository']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'sa-repository',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': 'Gasper3',
    'author_email': 'trzecik65@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Gasper3/sa-repository',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
