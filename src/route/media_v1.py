# controller router for processing resources, like picture, video, file etc.

from fastapi import APIRouter, Request, HTTPException, Header, UploadFile
from starlette.responses import HTMLResponse, FileResponse
from entity.dto.media_dto import MediaGetDto
from service.MediaService import media_service
from component.LogManager import log_manager
from common.response import OkResponse, ServerErrorResponse


log = log_manager.get_logger(__name__)

router = APIRouter()

@router.post("/upload")
async def upload_media(files: list[UploadFile]):
    """
    upload file to the server
    the uploaded file needs to have a filename and valid Conatent-Type tag, otherwise the file will reject
    :return: a json response with media_id
    """

    media_id_list = []

    for file in files:
        try:
            media_id = await media_service.upload_file(file=file)
            media_id_list.append(media_id)
        except Exception as e:
            return ServerErrorResponse(msg=f"upload file error, filename={file.filename}, err: {e}")

    return OkResponse(msg="upload done", data={"media_id": media_id_list})


@router.get("/{media_id}")
async def get_media(media_id: str):
    """
    get media by media id
    :param media_id:
    :return:
    """
    try:
        media_dto: MediaGetDto = await media_service.get_by_media_id(media_id)
        return FileResponse(media_type=media_dto.content_type, filename=media_dto.file_name, path=media_dto.file_path)
    except Exception as e:
        log.error(f"get file error, media_id={media_id}, err: {e}")
        return ServerErrorResponse(msg=f"get file error, media_id={media_id}, err: {e}")


@router.get("/test_page")
async def test_page():
    """
    page for testing purpose
    :return:
    """
    content = """
<form action="/api/media/v1/upload" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)