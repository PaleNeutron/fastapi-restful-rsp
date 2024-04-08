from functools import wraps
import inspect
from typing import Any, Callable, Optional, get_type_hints

from fastapi import HTTPException, Response

from fastapi.responses import JSONResponse
from pydantic import create_model

from fastapi_restful_rsp.models import BaseRestFulRsp, DataT, RspGereric

from logging import getLogger


logger = getLogger("fastapi.restful_rsp")


def default_code_callback(e: Exception = None) -> int:
    if isinstance(e, HTTPException):
        return e.status_code
    elif isinstance(e, Exception):
        return 500
    else:
        return 0


def create_restful_rsp_decorator(
    data_name: str,
    message_name: str,
    param_dict: dict[str, tuple[type, Any]] = None,
    code_name: str = "code",
    code_callback: Callable[[Optional[Exception]], int] = default_code_callback,
) -> Callable[..., Callable]:
    """
    Create a decorator that converts the return value of a function into a RestFulRsp object.

    Args:
        data_name (str): The name of the data field in the RestFulRsp object.
        message_name (str): The name of the message field in the RestFulRsp object.
        param_dict (dict[str, tuple[type, Any]]): A dictionary of additional parameters and their types for the RestFulRsp object.
        code_name (str, optional): The name of the code field in the RestFulRsp object. Defaults to "code".
        code_callback (Callable[[Optional[Exception]], int], optional): A callback function that returns the code value for the RestFulRsp object. Defaults to default_code_callback.

    Returns:
        Callable[..., Callable]: A decorator function that wraps another function and converts its return value into a RestFulRsp object.

    """
    if param_dict is None:
        param_dict = {}
    fields = {data_name: (DataT, None), message_name: (str, "")}
    if code_name:
        fields[code_name] = (get_type_hints(code_callback)["return"], 0)
    fields.update(param_dict)

    RestFulRsp = create_model("RestFulRsp", __base__=(RspGereric,), **fields)

    def handle_response(result, e=None):
        if isinstance(result, Response):
            return result
        if e:
            logger.exception(e)
            ret = {
                code_name: code_callback(e),
                message_name: str(e.detail if isinstance(e, HTTPException) else e),
            }
            ret_data = RestFulRsp[DataT](**ret)
            status_code = e.status_code if isinstance(e, HTTPException) else 500
            return JSONResponse(content=ret_data.model_dump(), status_code=status_code)
        else:
            ret = {data_name: result, code_name: code_callback()}
            return RestFulRsp[DataT](**ret)

    def restful_response(
        func: Callable[..., DataT],
    ) -> Callable[..., BaseRestFulRsp[DataT]]:
        """
        Decorator function that wraps another function and converts its return value into a RestFulRsp object.

        Args:
            func (Callable[..., DataT]): The function to be decorated.

        Returns:
            Callable[..., BaseRestFulRsp[DataT]]: The decorated function that returns a RestFulRsp object.

        Raises:
            Exception: If an error occurs during the execution of the decorated function.

        """

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return handle_response(result)
            except Exception as e:
                return handle_response(None, e)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return handle_response(result)
            except Exception as e:
                return handle_response(None, e)

        if inspect.iscoroutinefunction(func):
            wrapper = async_wrapper
        else:
            wrapper = sync_wrapper

        # change the return type of the function to  -> RestFulRsp[DataT]
        wrapper.__annotations__["return"] = RestFulRsp[
            wrapper.__annotations__.get("return", Any)
        ]
        if hasattr(func, "__signature__"):
            # change return type of the function signature
            # see https://docs.python.org/3/library/inspect.html#inspect.signature
            # if has a __signature__ attribute, this function returns it without further computations
            wrapper.__signature__ = func.__signature__.replace(
                return_annotation=wrapper.__annotations__["return"]
            )

        return wrapper

    return restful_response
