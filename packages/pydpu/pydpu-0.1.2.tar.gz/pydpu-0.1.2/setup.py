# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydpu', 'pydpu.proto', 'pydpu.proto.v1']

package_data = \
{'': ['*']}

install_requires = \
['Click>=8.1,<9.0',
 'google-api-core>=2.11.0,<3.0.0',
 'google>=3.0.0,<4.0.0',
 'grpcio>=1.51.1,<2.0.0']

entry_points = \
{'console_scripts': ['dpu = pydpu.cli:main']}

setup_kwargs = {
    'name': 'pydpu',
    'version': '0.1.2',
    'description': 'Python library and cli to communicate with DPUs and IPUs',
    'long_description': '# pydpu\n\n[![License](https://img.shields.io/github/license/opiproject/pydpu?style=flat&color=blue&label=License)](https://github.com/opiproject/pydpu/blob/main/LICENSE)\n[![Pulls](https://img.shields.io/docker/pulls/opiproject/pydpu.svg?logo=docker&style=flat&label=Pulls)](https://hub.docker.com/r/opiproject/pydpu)\n[![PyPI](https://img.shields.io/pypi/v/pydpu)](https://pypi.org/project/pydpu/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/opiproject/pydpu/branch/main/graph/badge.svg)](https://codecov.io/gh/opiproject/pydpu)\n[![Linters](https://github.com/opiproject/pydpu/actions/workflows/linters.yml/badge.svg)](https://github.com/opiproject/pydpu/actions/workflows/linters.yml)\n[![Docker](https://github.com/opiproject/pydpu/actions/workflows/docker.yaml/badge.svg)](https://github.com/opiproject/pydpu/actions/workflows/docker.yaml)\n[![Tests](https://github.com/opiproject/pydpu/actions/workflows/test.yaml/badge.svg)](https://github.com/opiproject/pydpu/actions/workflows/test.yaml)\n\nPython library and cli to communicate with DPUs and IPUs\n\n## I Want To Contribute\n\nThis project welcomes contributions and suggestions.  We are happy to have the Community involved via submission of **Issues and Pull Requests** (with substantive content or even just fixes). We are hoping for the documents, test framework, etc. to become a community process with active engagement.  PRs can be reviewed by by any number of people, and a maintainer may accept.\n\nSee [CONTRIBUTING](https://github.com/opiproject/opi/blob/main/CONTRIBUTING.md) and [GitHub Basic Process](https://github.com/opiproject/opi/blob/main/doc-github-rules.md) for more details.\n\n## Installation\n\nThere are several ways of running this CLI.\n\n### Docker\n\n```sh\ndocker pull opiproject/pydpu:<version>\n```\n\nYou can specify a version like `0.1.1` or use `latest` to get the most up-to-date version.\n\nRun latest version of the CLI in a container:\n\n```sh\ndocker run --rm opiproject/pydpu:latest --help\n```\n\nReplace `--help` with any `pydpu` command, without `pydpu` itself.\n\n### PyPI\n\n```sh\npip install pydpu\n```\n\n## Usage\n\n### Inventory\n\nTo get inventory, run:\n\n```sh\npydpu --address=localhost:50151 inventory get\n```\n\n### Ipsec\n\nTo create a tunnel, run:\n\n```sh\npydpu --address=localhost:50151 ipsec create-tunnel\n```\n\nTo get statistics, run:\n\n```sh\npydpu --address=localhost:50151 ipsec stats\n```\n\n## Packaging\n\nThis project uses [poetry](https://python-poetry.org/) to manage dependencies, build, etc.\n\n## Releasing new versions\n\n```sh\n# Make sure you have dev dependencies installed\n$ poetry install --group dev\n# Use bump2version to update version strings and create a new tag\n$ bump2version <patch|minor|major>\n# Push new tag\n$ git push --tags\n# Create GitHub release\n$ gh release create v$(poetry version -s) --generate-notes\n```\n',
    'author': 'OPI Dev',
    'author_email': 'opi-dev@lists.opiproject.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
