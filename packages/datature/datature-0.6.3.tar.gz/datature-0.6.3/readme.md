# Datatue Python SDK

## Get started

- [Documentation](#documentation)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Unit Test](#unit-test)

## Documentation

See the [API docs](https://developers.datature.io/).

## Installation

```sh
pip install --upgrade datature
```

### Requirements

- Python 3.7+

## Usage

The library needs to be configured with your project's secret key whihc is available in your Project Dashboard `Advanced/API Management`

```python
import datature
datature.project_secret = "6874c3c9b..."

# retrieve project
project = datature.Project.retrieve()

# print project information
print(project)

# retrieve project insight
insight = datature.Project.insight()

# print insight details
print(insight)

# list all assets
assets = datature.Asset.list()

# print the assets
print(assets)
```

## Unit Test

To run the tests, run command:

```sh
python -m coverage run -m unittest
```
