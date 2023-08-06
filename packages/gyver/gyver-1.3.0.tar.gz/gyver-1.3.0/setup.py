# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gyver',
 'gyver.boto',
 'gyver.boto.simple_queue',
 'gyver.cache',
 'gyver.config',
 'gyver.config.adapter',
 'gyver.context',
 'gyver.context.atomic_',
 'gyver.context.interfaces',
 'gyver.crypto',
 'gyver.database',
 'gyver.database.context',
 'gyver.database.drivers',
 'gyver.database.query',
 'gyver.database.session.asgi',
 'gyver.future',
 'gyver.future.utils',
 'gyver.url',
 'gyver.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'cryptography>=38.0.4,<39.0.0',
 'orjson>=3.8.1,<4.0.0',
 'pydantic[email]>=1.10.2,<2.0.0',
 'typing-extensions>=4.4.0,<5.0.0']

extras_require = \
{':sys_platform != "linux"': ['tzdata>=2022.6,<2023.0'],
 'cache': ['redis>=4.4.0,<5.0.0'],
 'db-mariadb': ['pymysql>=1.0.2,<2.0.0', 'asyncmy>=0.2.5,<0.3.0'],
 'db-mysql': ['pymysql>=1.0.2,<2.0.0', 'asyncmy>=0.2.5,<0.3.0'],
 'db-pg': ['psycopg2>=2.9.5,<3.0.0', 'asyncpg>=0.27.0,<0.28.0'],
 'db-sqlite': ['aiosqlite>=0.18.0,<0.19.0'],
 'sqlalchemy': ['sqlalchemy>=1.4.43,<2.0.0']}

setup_kwargs = {
    'name': 'gyver',
    'version': '1.3.0',
    'description': 'Toolbox for web development',
    'long_description': '# Gyver\n\n> Simple toolbox for python development to skip code boilerplate.\n\n[**Documentation**](https://guscardvs.github.io/gyver/)\n\n[**Source Code**](https://github.com/guscardvs/gyver)\n\n## Authors\n\n> [@guscardvs](https://github.com/guscardvs)\n\n## Requirements\n\n* Python 3.9+\n\n## Required\n\n* [OrJSON](https://github.com/ijl/orjson) for json parsing.\n* [Pydantic](https://docs.pydantic.dev) for data handling.\n* [Typing Extensions](https://github.com/python/typing_extensions) for compatibility.\n* [Cryptography](https://cryptography.io) to handle encryption.\n\n## Optional\n\nTo use the database parts:\n* **Mysql/MariaDB:** AsyncMy, PyMySQL (use db-mysql or db-mariadb extras)\n* **Postgres:** AsyncPG, Psycopg2\n* **SQLite:** aiosqlite\n* **Redis:** redis\n* And **SQLAlchemy**\n\n## Installation\n\n```console\n$ pip install gyver\n```\n\n## Roadmap\n\n> Migrate from pydantic to dataclass/attrs for a lighter version of the library\n\n##  License\n\nThis project is licensed under the terms of the MIT license.',
    'author': 'Gustavo Correa',
    'author_email': 'self.gustavocorrea@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guscardvs/gyver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
