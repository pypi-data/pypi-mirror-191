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
    'version': '0.2.0',
    'description': 'module provide manipulation with privileges with sqlalchemy',
    'long_description': '# Privileges manipulation with SQLalchemy\n\nAdd `grant/revoke privileges` construct\n\n## Usage\n\nExamples:\n```python\n>>> from sqlalchemy import *\n>>> from sqlalchemy_privileges import *\n\n>>> str(GrantPrivileges(\'insert\', Table(\'a\', MetaData(schema=\'schema\')), \'my.name\'))\n\'GRANT INSERT ON schema.a TO "my.name"\\n\'\n\n>>> str(RevokePrivileges([\'insert\', \'update\'], table(\'a\'), [\'my.name\', \'my.friend\']))\n\'REVOKE INSERT, UPDATE ON a TO "my.name", "my.friend"\\n\'\n\n>>> str(GrantPrivileges(\'all\', table(\'a\'), [\'my.name\', \'my.friend\']))\n\'GRANT ALL ON a TO "my.name", "my.friend"\\n\'\n```\n\n## Installation\n\n`sqlalchemy-privileges` is available on PyPI and can be installed via `pip`\n\n```console\npip install sqlalchemy-privileges\n```\n\n## Acknowledgements\nPackage inspired by [sqlalchemy-views](https://pypi.org/project/sqlalchemy-views/) \n\nAnd thank you to the various [contributors](https://github.com/GrozniyToaster/sqlalchmey-privileges/pulse)!',
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
