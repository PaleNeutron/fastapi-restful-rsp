from typing import Any, Callable, Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


DataT = TypeVar("DataT")


class RspGereric(GenericModel, Generic[DataT]):
    pass


class BaseRestFulRsp(BaseModel, Generic[DataT]):
    code: int = 0
    data: Optional[DataT] = None
    message: str = ""


RestFulRsp = BaseRestFulRsp