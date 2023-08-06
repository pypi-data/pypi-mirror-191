# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bioto_client',
 'bioto_client.domain',
 'bioto_client.infrastructure',
 'bioto_client.infrastructure.auth',
 'bioto_client.infrastructure.repository',
 'bioto_client.infrastructure.users']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=4.0.0,<5.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'requests>=2.28.2,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['bioto-client = bioto_client.cli:app']}

setup_kwargs = {
    'name': 'bioto-client',
    'version': '0.1.2',
    'description': 'A python CLI client for accessing Bioto data',
    'long_description': '# PyClient\n\nPython Client for retrieving Bioto sensor data\n\n## Goals\n\n### Auth0 login\n\n- [x] As a user I can login via auth0 to get a valid access token\n\nBoth of these steps can be accomplished by enabling device authentication.\n\n### Retrieving sensor data\n\n- [x] As a user I can find a garden\n- [ ] As a user I can subscribe to that garden\n- [ ] As a user I can see my subscribtion state for that garden\n  (pending/approved/declined)\n- [ ] As a iser I can get an overview of "my gardens"\n- [ ] As a user I can retrieve sensor data from my gardens\n  - current\n  - raw data up to 7 days ago\n  - downsampled data when more than 7 days ago\n\n## Getting started\n\nSoftware is installed via make (see below), this will setup a [virtual python\nenvironments][3] managed via [`poetry`][4]\n\n```bash\n% pip install --user bioto-client\n```\n\n## How to use\n\nWhen not installed as a python package but via `make install` run `poetry shell`\nfrom the root of the project first. Otherwise the first step can be skipped.\n\n```bash\n\n# Call the client with the `user` command to assert a valid session\n% bioto-client user\n\nLoading session\n\nNot logged in, please take the following steps:\n\n1. On your computer or mobile device navigate to: https://biotoco.eu.auth0.com/activate?user_code=NEWT-OKEN\n2. Enter the following code:  NEWT-OKEN\n\nSuccesfully logged in.\n\nBioto CLI client\nSession token ***5OFd09w\n```\n\n## Improve the client\n\nIf you want to improve the client or add something which you think is missing to\nthe project you can either [open an issue][1] or develop the feature yourself\nand open [a pull request with your changes][2].\n\nTo get started clone this project and create a branch. Now fix the bug or create\nthe feature you want and write some tests for it to prove it works. This can be\ndone by executing:\n\n```bash\n% make check\n```\n\n> **Note** This will run both tests and linters, use `make test` when you\'re in\n`red - green - refactor` mode\n\nWhen the checks are all passing and you\'ve committed your changes, you can push\nthese by running:\n\n```bash\n% make dist\n```\n\n[1]: https://github.com/wearebioto/PyClient/issues\n[2]: https://github.com/wearebioto/PyClient/pulls\n[3]: https://docs.python.org/3/library/venv.html\n[4]: https://python-poetry.org/docs/\n',
    'author': 'Bioto',
    'author_email': 'it@bioto.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
