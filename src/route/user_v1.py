from fastapi import APIRouter, Request, HTTPException, Header
from common.response import OkResponse
router = APIRouter()


@router.get("/test")
def test():
    return OkResponse(msg="test ok")