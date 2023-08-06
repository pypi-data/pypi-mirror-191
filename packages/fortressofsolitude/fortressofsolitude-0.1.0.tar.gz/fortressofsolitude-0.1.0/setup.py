# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fortressofsolitude']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4==4.11.1', 'pyyaml>=6.0,<7.0', 'requests==2.28.1']

setup_kwargs = {
    'name': 'fortressofsolitude',
    'version': '0.1.0',
    'description': 'A client to retrieve new releases of comic books, filterable by publisher and format.',
    'long_description': "# Fortress of Solitude\n\n<!-- TOC -->\n* [Fortress of Solitude](#fortress-of-solitude)\n  * [Requirements](#requirements)\n* [Project Expectations](#project-expectations)\n  * [How to get started](#how-to-get-started)\n    * [Create a virtual environment](#create-a-virtual-environment)\n    * [Enter virtual environment](#enter-virtual-environment)\n    * [Install Poetry, the package manager for this project](#install-poetry-the-package-manager-for-this-project)\n  * [Running Unit Tests](#running-unit-tests)\n    * [Pytest to run all unit tests in `test/`](#pytest-to-run-all-unit-tests-in-test)\n    * [Pytest to run all unit tests and lint code with `Pylama`](#pytest-to-run-all-unit-tests-and-lint-code-with-pylama)\n  * [Linting](#linting)\n  * [Roadmap](#roadmap)\n<!-- TOC -->\n## Why is this project called the Fortress of Solitude\nHonestly just thought a library like this needs 1. A cool name and 2. Something comic book related\n\n## What is the Fortress of Solitude in Comic Books? \nFrom the DC Fandom Wiki: \n> The Fortress of Solitude is a home base for Superman and by extension, other heroes in the Superman Family. It is usually located in the one of the poles and uses serves as a place to store weapons and machinery from Krypton.\n## Requirements\n- Python 3.9 or above\n- Virtualenv 20.14.1 or above\n\n# Project Expectations\n- Client library to get new releases, or releases for a given date. \n- Client can filter by the format of releases e.g. 'single-issue' or by publisher e.g. 'marvel'\n- Client should be straight forward and easy to use by using the KISS model (Keep It Simple Stupid)\n- Cache results where possible as not to hit provider with too many requests for the same data\n\n## How to get started\n### Create a virtual environment\n```bash\nvirtualenv -p python3.9 venv\n```\n\n### Enter virtual environment\n```bash\nsource venv/bin/activate\n```\n\n### Install Poetry, the package manager for this project\n```bash\npip install poetry\n```\n\n## Running Unit Tests\n### Pytest to run all unit tests in `test/`\n```bash\npytest\n```\n\n### Pytest to run all unit tests and lint code with `Pylama`\n```bash\npytest --pylama\n```\n\n## Linting\nThis project strives to keep the code style in line with [PEP8](https://peps.python.org/pep-0008/).\nTo test the project for compliance with PEP8, I use [Pylama](https://github.com/klen/pylama)\n```bash\npip install pylama\n```\n```bash\npylama fortressofsolitude\n```\n***\n## Roadmap\n- [ ] Database to cache results from source\n- [ ] Sphinx Automatic Documentation Creation",
    'author': 'Aaron Steed',
    'author_email': 'asteed7@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
