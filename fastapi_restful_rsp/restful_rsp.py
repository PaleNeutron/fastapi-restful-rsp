from functools import wraps
import inspect
from typing import Callable, Generic, TypeVar

from fastapi import HTTPException

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from logging import getLogger


logger = getLogger("fastapi.restful_rsp")

DataT = TypeVar("DataT")


# define RestFulRsp
class RestFulRsp(BaseModel, Generic[DataT]):
    code: int = 200
    data: DataT = None
    message: str = ""


def restful_response(func: Callable[..., DataT]) -> Callable[..., RestFulRsp[DataT]]:
    """
    Decorator function that wraps another function and converts its return value into a RestFulRsp object.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function that returns a RestFulRsp object.

    Raises:
        Exception: If an error occurs during the execution of the decorated function.

    """
    # check func is a coroutine function
    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return RestFulRsp[DataT](data=result)
            except HTTPException as e:
                logger.exception(e)
                ret_data = RestFulRsp[DataT](code=e.status_code, status="error", message=e.detail)
                return JSONResponse(content=ret_data.model_dump(), status_code=e.status_code)
            except Exception as e:
                logger.exception(e)
                ret_data = RestFulRsp[DataT](code=500, status="error", message=str(e))
                return JSONResponse(content=ret_data.model_dump(), status_code=500)

    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return RestFulRsp[DataT](data=result)
            except HTTPException as e:
                logger.exception(e)
                ret_data = RestFulRsp[DataT](code=e.status_code, status="error", message=e.detail)
                return JSONResponse(content=ret_data.model_dump(), status_code=e.status_code)
            except Exception as e:
                logger.exception(e)
                ret_data = RestFulRsp[DataT](code=500, status="error", message=str(e))
                return JSONResponse(content=ret_data.model_dump(), status_code=500)

    # change the return type of the function to  -> RestFulRsp[DataT]
    wrapper.__annotations__["return"] = RestFulRsp[wrapper.__annotations__["return"]]
    if hasattr(func, "__signature__"):
        # change return type of the function signature
        # see https://docs.python.org/3/library/inspect.html#inspect.signature
        # if has a __signature__ attribute, this function returns it without further computations
        wrapper.__signature__ = func.__signature__.replace(
            return_annotation=wrapper.__annotations__["return"]
        )

    return wrapper
