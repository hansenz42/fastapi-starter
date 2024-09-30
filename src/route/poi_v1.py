# routers for process poi information, and poi crud

from fastapi import APIRouter, Request, HTTPException, Header
from common.response import OkResponse
from entity.dto.poi_dto import *
from service.PoiService import poi_service

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
def add_poi(dto: AddPoiRequestDto):
    """
    router for recording new poi
    :return:
    """
    return poi_service.add_new_poi(dto)