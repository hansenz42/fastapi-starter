from datetime import datetime

from common.uuid import gen_uuid
from dao.PoiDao import poi_dao
from entity.dto.poi_dto import AddPoiRequestDto, PoiResponseDto
from entity.po.PoiPo import PoiPo


class PoiService:

    def __init__(self):
        pass

    async def add_new_poi(self, dto: AddPoiRequestDto):
        new_uuid = 'POI_' + gen_uuid()
        await poi_dao.add_po(
            uuid=new_uuid,
            name=dto.name,
            lat=dto.lat,
            long=dto.long,
            ssid=dto.ssid,
            text_content=dto.content,
            img_list=dto.img_list
        )
        return new_uuid

    async def get_poi_by_uuid(self, uuid: str) -> PoiResponseDto:
        po = await poi_dao.get_w_uuid(uuid)
        return PoiResponseDto(
            uuid=po.uuid,
            name=po.name,
            lat=po.lat,
            long=po.long,
            ssid=po.ssid,
            content=po.text_content,
            img_list=po.img_list
        )

    async def match_by_poi(self, poi_id: str, media_id: str):
        """
        match poi and media
        :param poi_id:
        :param media_id:
        :return:
        """
        # 1. get poi images

        # 2. match poi images one by one

        # 3. get highest similarity score

        # 4. if similarity score > 0.1, return good else return bad


poi_service: PoiService = PoiService()

import sys

if 'pytest' in sys.modules:
    import pytest

    @pytest.mark.asyncio
    async def test_add_new_poi():
        ret = await poi_service.add_new_poi(
            AddPoiRequestDto(
                name='test_poi1',
                lat=0,
                long=0,
                ssid='test_poi1',
                content='test_poi1',
                img_list='[]'
            )
        )
        print(ret)