# controller router for processing resources, like picture, video, file etc.

from fastapi import APIRouter, Request, HTTPException, Header, UploadFile
from starlette.responses import HTMLResponse

from common.response import OkResponse

router = APIRouter()

@router.post("/upload")
def upload_media(files: list[UploadFile]):
    """
    :return:
    """
    return OkResponse(msg="upload ok")


@router.get("/page")
async def main():
    content = """
<form action="/api/media/v1/upload" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)