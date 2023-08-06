# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lex_core',
 'lex_core.commands',
 'lex_core.dtos',
 'lex_core.tests',
 'lex_core.value_objects']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'ulid-py>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'karp-lex-core',
    'version': '0.3.2',
    'description': 'The core of karp-lex',
    'long_description': '# karp-lex-core\n\n- **karp-lex-core** [![PyPI version](https://badge.fury.io/py/karp-lex-core.svg)](https://badge.fury.io/py/karp-lex-core)\n\nThe core for karp-lex\n\nContains commands, entry_dto and unique_id for `karp.lex` in `karp.backend`.\n\n',
    'author': 'Språkbanken at the University of Gothenburg',
    'author_email': 'sb-info@svenska.gu.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://spraakbanken.gu.se',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
