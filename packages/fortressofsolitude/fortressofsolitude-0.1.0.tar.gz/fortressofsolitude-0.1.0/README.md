# Fortress of Solitude

<!-- TOC -->
* [Fortress of Solitude](#fortress-of-solitude)
  * [Requirements](#requirements)
* [Project Expectations](#project-expectations)
  * [How to get started](#how-to-get-started)
    * [Create a virtual environment](#create-a-virtual-environment)
    * [Enter virtual environment](#enter-virtual-environment)
    * [Install Poetry, the package manager for this project](#install-poetry-the-package-manager-for-this-project)
  * [Running Unit Tests](#running-unit-tests)
    * [Pytest to run all unit tests in `test/`](#pytest-to-run-all-unit-tests-in-test)
    * [Pytest to run all unit tests and lint code with `Pylama`](#pytest-to-run-all-unit-tests-and-lint-code-with-pylama)
  * [Linting](#linting)
  * [Roadmap](#roadmap)
<!-- TOC -->
## Why is this project called the Fortress of Solitude
Honestly just thought a library like this needs 1. A cool name and 2. Something comic book related

## What is the Fortress of Solitude in Comic Books? 
From the DC Fandom Wiki: 
> The Fortress of Solitude is a home base for Superman and by extension, other heroes in the Superman Family. It is usually located in the one of the poles and uses serves as a place to store weapons and machinery from Krypton.
## Requirements
- Python 3.9 or above
- Virtualenv 20.14.1 or above

# Project Expectations
- Client library to get new releases, or releases for a given date. 
- Client can filter by the format of releases e.g. 'single-issue' or by publisher e.g. 'marvel'
- Client should be straight forward and easy to use by using the KISS model (Keep It Simple Stupid)
- Cache results where possible as not to hit provider with too many requests for the same data

## How to get started
### Create a virtual environment
```bash
virtualenv -p python3.9 venv
```

### Enter virtual environment
```bash
source venv/bin/activate
```

### Install Poetry, the package manager for this project
```bash
pip install poetry
```

## Running Unit Tests
### Pytest to run all unit tests in `test/`
```bash
pytest
```

### Pytest to run all unit tests and lint code with `Pylama`
```bash
pytest --pylama
```

## Linting
This project strives to keep the code style in line with [PEP8](https://peps.python.org/pep-0008/).
To test the project for compliance with PEP8, I use [Pylama](https://github.com/klen/pylama)
```bash
pip install pylama
```
```bash
pylama fortressofsolitude
```
***
## Roadmap
- [ ] Database to cache results from source
- [ ] Sphinx Automatic Documentation Creation