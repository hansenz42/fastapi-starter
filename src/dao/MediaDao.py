from datetime import datetime

from sqlalchemy import select

from entity.po.MediaPo import MediaPo
from component.SqlConnectorManager import sql_connection_manager

class MediaDao:
    def __init__(self):
        self.__session_maker = sql_connection_manager.get_session_maker()

    async def add_media(self, uuid: str, file_name: str, content_type: str, url: str):
        async with self.__session_maker() as session:
            media = MediaPo()
            media.uuid = uuid
            media.file_name = file_name
            media.content_type = content_type
            media.url = url
            media.created_at = datetime.now()
            media.modified_at = datetime.now()
            session.add(media)
            await session.commit()

    async def get_media_by_media_id(self, uuid: str) -> MediaPo:
        async with self.__session_maker() as session:
            p = select(MediaPo).filter_by(uuid=uuid)
            result = await session.execute(p)
            return result.scalar()



media_dao: MediaDao = MediaDao()