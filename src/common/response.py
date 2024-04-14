from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union


def res_ok(*, data: Union[list, dict, str] = None) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'msg': "ok",
            'data': data,
        }
    )


def res_error(*, code: int=-1, msg: str = "服务器错误") -> Response:
    """
    带 code 的自定义错误
    :param code:
    :param msg:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'code': code,
            'msg': msg
        }
    )


def res_bad_request(*, msg: str = "参数错误") -> Response:
    """
    参数相关错误
    :param msg:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 400,
            'msg': msg
        }
    )


def res_server_error(*, message: str = "服务器错误") -> Response:
    """
    服务器错误
    :param message:
    :return:
    """
    return res_error(code=500, msg=message)
