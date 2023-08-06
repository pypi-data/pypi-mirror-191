# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_privileges']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.0.0']

setup_kwargs = {
    'name': 'sqlalchemy-privileges',
    'version': '0.1.0',
    'description': 'module provide manipulation with privileges with sqlalchemy',
    'long_description': '',
    'author': 'Nedosekov Ivan',
    'author_email': 'ivan-nedd@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/GrozniyToaster/sqlalchmey-privileges',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
