from component.SqlConnectorManager import sql_connection_manager
from entity.po.PoiIdentifyImagePo import PoiWIdentifyImagePo
from sqlalchemy import select
from datetime import datetime


class PoiWIdentifiedImageDao:
    def __init__(self):
        self.__session_maker = sql_connection_manager.get_session_maker()

    async def add(self, image_url: str, algorithm: str, keypoints: bytes, descriptors: bytes, poi_uuid: str,
                  image_uuid: str):
        async with self.__session_maker() as session:
            po = PoiWIdentifyImagePo()
            po.poi_uuid = poi_uuid
            po.image_url = image_url
            po.algorithm = algorithm
            po.keypoints = keypoints
            po.descriptors = descriptors
            po.image_uuid = image_uuid
            po.created_at = datetime.now()
            po.modified_at = datetime.now()
            session.add(po)
            await session.commit()

    async def get_identified_image(self, image_uuid: str) -> PoiWIdentifyImagePo:
        async with self.__session_maker() as session:
            result = await session.execute(
                select(PoiWIdentifyImagePo).where(PoiWIdentifyImagePo.image_uuid == image_uuid))
            return result.scalar()

    async def get_identified_images_by_poi(self, poi_uuid: str) -> list[PoiWIdentifyImagePo]:
        async with self.__session_maker() as session:
            result = await session.execute(select(PoiWIdentifyImagePo).where(PoiWIdentifyImagePo.poi_uuid == poi_uuid))
            return result.scalars().all()


poi_w_identified_image_dao: PoiWIdentifiedImageDao = PoiWIdentifiedImageDao()

import sys

if 'pytest' in sys.modules:
    import pytest


    @pytest.mark.asyncio
    async def test_add_identified_image():
        pass
