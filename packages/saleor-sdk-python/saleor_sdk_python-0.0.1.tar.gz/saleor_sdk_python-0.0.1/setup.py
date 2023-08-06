# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['saleor_sdk',
 'saleor_sdk.console',
 'saleor_sdk.crypto',
 'saleor_sdk.crypto.tests',
 'saleor_sdk.schemas']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9',
 'cryptography>=38,<39',
 'pydantic>=1,<2',
 'pyjwt>=2,<3',
 'tomli>=2,<3']

entry_points = \
{'console_scripts': ['saleor-sdk = saleor_sdk.console.app:cli']}

setup_kwargs = {
    'name': 'saleor-sdk-python',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Saleor SDK Python\n\nA set of tools that help Python developers work with Saleor. This is a very early stage in the life of this library and many things are not yet figured out. \n\nDocumentation, contribution rules, process and the code itself (this includes the APIs) are expected to change rapidly.\n\n## Installation\n\nInstall [Poetry](https://python-poetry.org/docs/#installing-with-pipx).\n\nClone the repository and invoke:\n\n```\npoetry install\n```\n\n## Documentation\n\nIn the Poetry shell (`poetry shell` after installing the dependencies), run:\n\n```\nmkdocs serve\n```\n\nand navigate to http://127.0.0.1:8000\n\n## Tooling\n\nThis library provides a CLI that contains a growing set of commands that are useful in day-to-day development around Saleor.\n\nThere are two entrypoints (here is a [good article](https://snarky.ca/why-you-should-use-python-m-pip/) on why this is important):\n\n```sh\npython -m saleor_sdk tools\nsaleor_sdk tools\n```\n\n### Saleor ID encoding\n\n```sh\nsaleor-sdk tools decode-id VXNlcjoyMg==\nsaleor-sdk tools encode-id User 22\n```\n',
    'author': 'Paweł Kucmus',
    'author_email': 'pawel.kucmus@mirumee.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mirumee/saleor-sdk-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
