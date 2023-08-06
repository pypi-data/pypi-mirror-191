# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dc_avro']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'dataclasses-avroschema>=0.36.1,<0.37.0',
 'deepdiff>=6.2.3,<7.0.0',
 'httpx>=0.23.3,<0.24.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['dc-avro = dc_avro.main:app']}

setup_kwargs = {
    'name': 'dc-avro',
    'version': '0.6.0',
    'description': '',
    'long_description': "# Dataclasses Avro Schema CLI\n\nCommand line interface from [dataclasses-avroschema](https://github.com/marcosschroh/dataclasses-avroschema) to work with `avsc` resources\n\n[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fmarcosschroh%2Fdc-avro%2Fbadge%3Fref%3Dmaster&style=flat)](https://actions-badge.atrox.dev/marcosschroh/dc-avro/goto?ref=master)\n[![GitHub license](https://img.shields.io/github/license/marcosschroh/dc-avro.svg)](https://github.com/marcosschroh/dc-avro/blob/master/LICENSE)\n[![codecov](https://codecov.io/gh/marcosschroh/dc-avro/branch/master/graph/badge.svg)](https://codecov.io/gh/marcosschroh/dc-avro)\n![python version](https://img.shields.io/badge/python-3.7%2B-yellowgreen)\n\n## Requirements\n\n`python 3.7+`\n\n## Documentation\n\nhttps://marcosschroh.github.io/dc-avro/\n\n## Usage\n\nYou can validate `avro schemas` either from a `local file` or `url`:\n\nAssuming that we have a local file `schema.avsc` that contains an `avro schema`, we can check whether it is valid\n\n```bash\ndc-avro validate-schema --path schema.avsc\n\nValid schema!! 👍 \n\n{\n    'type': 'record',\n    'name': 'UserAdvance',\n    'fields': [\n        {'name': 'name', 'type': 'string'},\n        {'name': 'age', 'type': 'long'},\n        {'name': 'pets', 'type': {'type': 'array', 'items': 'string', 'name': 'pet'}},\n        {'name': 'accounts', 'type': {'type': 'map', 'values': 'long', 'name': 'account'}},\n        {'name': 'favorite_colors', 'type': {'type': 'enum', 'name': 'FavoriteColor', 'symbols': ['BLUE', 'YELLOW', 'GREEN']}},\n        {'name': 'has_car', 'type': 'boolean', 'default': False},\n        {'name': 'country', 'type': 'string', 'default': 'Argentina'},\n        {'name': 'address', 'type': ['null', 'string'], 'default': None},\n        {'name': 'md5', 'type': {'type': 'fixed', 'name': 'md5', 'size': 16}}\n    ]\n}\n```\n\nTo see all the commands execute `dc-avro --help`\n\n## Features\n\n* [x] Validate `schemas`\n* [x] Generate `models` from `schemas`\n* [x] Data deserialization with `schema`\n* [x] Data serialization with `schema`\n* [x] View diff between `schemas`\n* [] Generate fake data from `schema`\n\n## Development\n\n1. Install requirements: `poetry install`\n2. Code linting: `./scripts/format`\n3. Run tests: `./scripts/test`\n",
    'author': 'Marcos Schroh',
    'author_email': 'marcos.schroh@kpn.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
