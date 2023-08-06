# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hitfactorpy_sqlalchemy',
 'hitfactorpy_sqlalchemy.cli',
 'hitfactorpy_sqlalchemy.cli.model',
 'hitfactorpy_sqlalchemy.migrations',
 'hitfactorpy_sqlalchemy.migrations.versions',
 'hitfactorpy_sqlalchemy.migrations.versions copy',
 'hitfactorpy_sqlalchemy.orm']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.9.2,<2.0.0',
 'asyncpg>=0.27.0,<0.28.0',
 'hitfactorpy>=0.1.1,<0.2.0',
 'inflection>=0.5.1,<0.6.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'rich<13',
 'sqlalchemy-continuum>=1.3.14,<2.0.0',
 'sqlalchemy-utils>=0.39.0,<0.40.0',
 'sqlalchemy[asyncio,mypy]>=1.4,<2.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['hitfactorpy-sqlalchemy = hitfactorpy_sqlalchemy.cli:cli']}

setup_kwargs = {
    'name': 'hitfactorpy-sqlalchemy',
    'version': '0.0.5',
    'description': 'Manage practical match reports with SQLAlchemy',
    'long_description': '# hitfactorpy_sqlalchemy\n\n[![Main](https://github.com/cahna/hitfactorpy-sqlalchemy/actions/workflows/main.yaml/badge.svg)](https://github.com/cahna/hitfactorpy-sqlalchemy/actions/workflows/main.yaml)\n[![PyPI version](https://badge.fury.io/py/hitfactorpy-sqlalchemy.svg)](https://badge.fury.io/py/hitfactorpy-sqlalchemy)\n\nManage practical match reports in a database with SQLAlchemy\n\n## Status\n\n**Work in progress...**\n\n## Documentation\n\nSee `docs/index.md` via [website](https://cahna.github.io/hitfactorpy-sqlalchemy/) or [source](https://github.com/cahna/hitfactorpy-sqlalchemy/blob/main/docs/index.md).\n',
    'author': 'Conor Heine',
    'author_email': 'conor.heine@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
