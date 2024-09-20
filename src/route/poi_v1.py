from fastapi import APIRouter, Request, HTTPException, Header
from common.response import OkResponse
from pydantic import BaseModel
router = APIRouter()

class NearbyRequestDto(BaseModel):
    lat: float
    long: float

@router.get("/nearby")
def nearby():
    """
    router for nearby position of interest
    :return:
    """
    return OkResponse(msg="test ok")

class ImageRecRequestDto(BaseModel):
    lat: float
    long: float
    image: str

@router.post("/image-rec")
def image_rec():
    """
    router for image recognition api
    :return:
    """
