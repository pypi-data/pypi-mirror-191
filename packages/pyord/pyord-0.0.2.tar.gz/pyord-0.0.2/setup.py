# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.ord']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'httpx>=0.23.3,<0.24.0',
 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'pyord',
    'version': '0.0.2',
    'description': 'bitcoin jpegs',
    'long_description': '[![pypi](https://img.shields.io/pypi/v/pyord.svg)](https://pypi.python.org/pypi/pyord)\n\nA sandbox for working with [ord](https://github.com/casey/ord).\n\nFor now, api calls go through https://ordapi.xyz/ but an [official api is in the works](https://github.com/casey/ord/pull/1662). Will switch to that once available, or start wrapping the ord crate from python.\n\n## Setup\n\nClone, `poetry install` then `pre-commit install`.\n\n`poetry run pytest`\n\n\n## Usage\n\nAll subject to change. Just exploring the api for now.\n\nA simple example of iterating through inscriptions and printing any with plaintext content:\n\n```python\nfrom src.ord import client\n\nfor i, inscription_id in enumerate(client.inscription_ids(start=0, stop=100)):\n    inscription = client.get_content(inscription_id)\n    try:\n        plaintext = inscription.decode("utf-8")\n        print(i, inscription_id, "plaintext content")\n        print(plaintext, "\\n\\n")\n    except UnicodeDecodeError:\n        pass\n```\n',
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
