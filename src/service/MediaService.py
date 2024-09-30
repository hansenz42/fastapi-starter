class MediaService:
    def __init__(self):
        pass

    async def upload_file(self):
        """
        upload file to the server, and return file generated uuid。
        - save file to local filesystem
        - save file information to database
        :return:
        """
        pass

    async def get_file_by_media_id(self):
        """
        use media_id to return file binary file
        :return:
        """
        pass



media_service: MediaService = MediaService()

import sys

if 'pytest' in sys.modules:
    import pytest

    @pytest.mark.asyncio
    async def test_add_new_poi():
        pass