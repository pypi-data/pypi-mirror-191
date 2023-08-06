![GitHub](https://img.shields.io/github/license/surquest/python-utils-loader?style=flat-square)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/surquest/python-utils-loader/package-python.yml?branch=main&style=flat-square)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/surquest/6e25c317000917840152a5e702e71963/raw/python-utils-loader.json&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/surquest-utils-loader?style=flat-square)



# Introduction

Standalone Loader class simplifies loading of content from files `.yaml`, `.json`, `.sql`, and `.txt`.

# Quick Start

```python
# import the Loader class
from surquest.utils.loader import Loader

# load a yaml file
config_yaml = Loader.load(path="./path/to/config.yaml")
# alternatively load of yaml file
config_yaml = Loader.load_yaml(path="./path/to/config.yaml")

# load a json file
config_json = Loader.load(path="./path/to/config.json")
# alternatively load of json file
config_json = Loader.load_json(path="./path/to/config.json")

# load a sql file
config_sql = Loader.load(path="./path/to/config.sql")
# alternatively load of sql file
config_sql = Loader.load_sql(path="./path/to/config.sql")
```

# Local development

You are more than welcome to contribute to this project. To make your start easier we have prepared a docker image with all the necessary tools to run it as interpreter for Pycharm or to run tests.


## Build docker image
```
docker build `
     --tag surquest/utils/loader `
     --file package.base.dockerfile `
     --target test .
```

## Run tests
```
docker run --rm -it `
 -v "${pwd}:/opt/project" `
 -w "/opt/project/test" `
 surquest/utils/loader pytest
```