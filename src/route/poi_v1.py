# routers for process poi information, and poi crud

from fastapi import APIRouter, Request, HTTPException, Header
from common.response import OkResponse, ServerErrorResponse
from entity.dto.poi_dto import *
from service.PoiService import poi_service
from component.LogManager import log_manager


log = log_manager.get_logger(__name__)

router = APIRouter()

@router.get("/nearby")
def nearby():
    """
    router for nearby position of interest
    :return:
    """
    return OkResponse(msg='test ok')

@router.post("/image-rec")
def image_rec():
    """
    router for image recognition api
    :return:
    """
    return OkResponse(msg='test ok')


@router.post("/poi")
async def add_poi(dto: AddPoiRequestDto):
    """
    router for recording new poi
    :return:
    """
    try:
        new_uuid = await poi_service.add_new_poi(dto)
        return OkResponse(msg='ok', data={'poi_id': new_uuid})
    except Exception as e:
        log.error(f"add poi error, err: {e}")
        return ServerErrorResponse(msg=f"add poi error, err: {e}")