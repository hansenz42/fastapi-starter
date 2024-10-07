from hmac import trans_36
from typing import BinaryIO

from fastapi import UploadFile
from common.uuid import gen_uuid
from component.FileManager import file_manager
from dao.MediaDao import media_dao
from entity.dto.media_dto import MediaGetDto


class MediaService:
    def __init__(self):
        pass

    async def upload_file(self, file: UploadFile) -> str:
        """
        upload file to the server, and return file generated uuid。
        - media id will generated for each media file
        - save file to local filesystem, to defined file path
        - save file information to database, media table
        :return: media_id of this file
        """
        media_id = f'MEDIA_{gen_uuid()}'
        # save file to filesystem
        try:
            file_path = file_manager.save_binary(file=file.file, file_name=media_id)
        except Exception as e:
            raise IOError(f"cannot save file, filename={file.filename}, err: {e}")

        # record to database
        try:
            await media_dao.add_media(uuid=media_id, file_name=file.filename, content_type=file.content_type, url='file:/'+file_path)
        except Exception as e:
            raise Exception(f"cannot save file, cannot write to database, filename={file.filename}, err: {e}")
        return media_id

    async def get_file_by_media_id(self, media_id: str)-> MediaGetDto:
        """
        use media_id to return file binary file
        :return:
        """
        # check file in database
        media = await media_dao.get_media_by_media_id(uuid=media_id)

        if media is None:
            # cannot find file
            return None

        file_path = media.url.split('file:/')[-1]

        return MediaGetDto(
            uuid=media.uuid,
            file_name=media.file_name,
            content_type=media.content_type,
            url=media.url,
            file_path=file_path
        )



media_service: MediaService = MediaService()

import sys

if 'pytest' in sys.modules:
    import pytest

    @pytest.mark.asyncio
    async def test_add_new_poi():
        pass