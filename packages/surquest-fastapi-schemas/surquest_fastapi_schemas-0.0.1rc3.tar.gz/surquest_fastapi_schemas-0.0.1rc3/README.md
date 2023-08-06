![GitHub](https://img.shields.io/github/license/surquest/python-fastapi-schemas?style=flat-square)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/surquest/python-fastapi-schemas/test.yml?branch=main&style=flat-square)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/surquest/6e25c317000917840152a5e702e71963/raw/python-fastapi-schemas.json&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/surquest-fastapi-schemas?style=flat-square)

# Introduction

This project provides collection of commonly used schemas for FastAPI.

# Quick Start

This section shows how to use the utilities provided by this project:

```python
from fastapi import FastAPI
from surquest.fastapi.schemas.args import Args

app = FastAPI()

@app.get("/users")
async def get_users(
        offset: Args.offset().type_ = Args.offset().query,
        limit: Args.limit().type_ = Args.limit().query,
):
    return [{
        "id": 1,
        "name": "John Doe"
    }]
```

# Local development

You are more than welcome to contribute to this project. To make your start easier we have prepared a docker image with all the necessary tools to run it as interpreter for Pycharm or to run tests.


## Build docker image
```
docker build `
     --tag surquest/fastapi/schemas `
     --file package.base.dockerfile `
     --target test .
```

## Run tests
```
docker run --rm -it `
 -v "${pwd}:/opt/project" `
 -w "/opt/project/test" `
 surquest/fastapi/schemas pytest
```