from typing import Generic, Optional, TypeVar

from pydantic import BaseModel


DataT = TypeVar("DataT")


class RspGereric(BaseModel, Generic[DataT]):
    pass


class BaseRestFulRsp(RspGereric):
    code: int = 0
    data: Optional[DataT] = None
    message: str = ""


RestFulRsp = BaseRestFulRsp
