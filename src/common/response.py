from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union


from typing import Union, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class OkResponse(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "ok"
    data: T | None = None


class ServerErrorResponse(BaseModel):
    code: int = 500
    msg: str = "server error"
    data: Union[list, dict, str, None]


class BadRequestResponse(BaseModel):
    code: int = 400
    msg: str = "bad request"
    data: Union[list, dict, str, None]
