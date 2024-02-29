# Wrap fastapi endpoints with RESTful API

Modern frontend frameworks encourage backend developers to follow RESTful API design. This package wraps fastapi endpoints with following structure:

```json
{
  "data": {
    ...
  },
  "code": 200,
  "message": ""
}
```

and modify fastapi generated OpenAPI documentation to reflect the change.

## Installation

```bash
pip install fastapi-restful-rsp
```

## Usage

```python
from fastapi import FastAPI
from fastapi_restful_rsp import restful_response

app = FastAPI()

@app.get("/foo/")
@restful_response
def foo()-> str:
    return "Hello World"
```
