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

@router.post("/match_by_poi")
async def match_by_poi(dto: MatchPoiRequestDto):
    """
    match poi by poi identify image self
    the photo taken will be matched by specific image of poi, if success, return good else return bad
    :return:
    """
    try:
        await poi_service.match_by_poi(dto.poi_id, dto.image_media_id)
    except Exception as e:
        log.error(f"match poi error, err: {e}")
        return ServerErrorResponse(msg=f"match poi error, err: {e}")

@router.post("/match_by_location")
async def match_by_location(dto: MatchLocationRequestDto):
    """
    match a poi by location (long and lat) and image
    :return:
    """

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