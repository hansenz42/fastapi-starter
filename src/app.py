import asyncio

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse, JSONResponse
from common.response import res_bad_request, res_error
from component.ConfigManager import config_manager

# 启动 FastAPI http 服务器
from component.LogManager import log_manager

logger = log_manager.get_logger("app")

app = FastAPI()

logger.info(f"服务已启动：version: {config_manager.get_value('version')}")

# 引入路由
from route.demo import router as demo_router
app.include_router(demo_router, prefix="/api/v1/demo", tags=["demo"])



@app.on_event("startup")
async def startup_event():
    logger.info("服务启动")


@app.get("/")
async def root():
    return f"服务已部署，version：{config_manager.get_value('version')}"

# 错误处理部分代码

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """
    错误处理 HTTP 错误，返回 http 400
    :param request:
    :param exc:
    :return:
    """
    logger.error(f"HTTP 错误: {exc}")
    return res_error(code=exc.status_code, msg="发生 http 错误")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    """
    错误处理，请求无效错误，返回 http 500
    :param request:
    :param exc:
    :return:
    """
    logger.warning(f"收到无效 body：{exc}")
    return res_bad_request(msg='无效body')
