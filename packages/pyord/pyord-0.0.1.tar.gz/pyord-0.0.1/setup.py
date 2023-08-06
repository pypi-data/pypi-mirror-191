# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.ord']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'pyord',
    'version': '0.0.1',
    'description': 'bitcoin jpegs',
    'long_description': 'A sandbox for working with [ord](https://github.com/casey/ord).\n\nFor now, api calls go through https://ordapi.xyz/ but an [official api is in the works](https://github.com/casey/ord/pull/1662). Will switch to that once available, or start wrapping the ord crate from python.\n\n## Setup\n\nClone, `poetry install` then `pre-commit install`.\n\n`poetry run pytest`\n',
    'author': 'Sam Barnes',
    'author_email': 'sam.barnes@opensea.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
