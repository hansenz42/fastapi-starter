from fastapi import APIRouter, Request, HTTPException, Header
from common.response import res_ok
router = APIRouter()


@router.get("/test")
def test():
    return res_ok()