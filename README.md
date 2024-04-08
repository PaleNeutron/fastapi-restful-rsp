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

### Custom response structure

You can customize the response structure by passing `data_name`, `code_key`, `message_name` to `restful_response` decorator.

```python
restful_response = create_restful_rsp_decorator(
    data_name="data", code_name="my_code", message_name="message", param_dict={"status": (str, "success")}
)

@app.get("/foo/")
@restful_response
def foo()-> str:
    return "Hello World"
```
