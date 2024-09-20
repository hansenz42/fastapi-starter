from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from common.response import BadRequestResponse, ServerErrorResponse
from component.ConfigManager import config_manager
from contextlib import asynccontextmanager

# 启动 FastAPI http 服务器
from component.LogManager import log_manager

logger = log_manager.get_logger("app")

app = FastAPI()

logger.info(f"service loaded: {config_manager.get_value('version')}")

from route.user_v1 import router as user_router
app.include_router(user_router, prefix="/api/user/v1", tags=["user"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("service started")
    yield
    logger.info("service stopped")


@app.get("/")
async def root():
    return f"service deployed，version：{config_manager.get_value('version')}"

# 错误处理部分代码


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """
    错误处理 HTTP 错误，返回 http 400
    :param request:
    :param exc:
    :return:
    """
    logger.error(f"HTTP error: {exc}")
    return ServerErrorResponse(code=exc.status_code, msg="http error")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    """
    错误处理，请求无效错误，返回 http 500
    :param request:
    :param exc:
    :return:
    """
    logger.warning(f"received invalid body：{exc}")
    return BadRequestResponse(msg="invalid body")
