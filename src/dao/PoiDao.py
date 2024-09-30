from datetime import datetime
from common.uuid import gen_uuid

from component.SqlConnectorManager import sql_connection_manager
from entity.po.PoiPo import PoiPo


class PoiDao:
    def __init__(self):
        self.__session_maker = sql_connection_manager.get_session_maker()

    async def add_po(self, name: str, lat: float, long: float, ssid: str, text_content: str, img_list: str):
        uuid = gen_uuid()
        async with self.__session_maker() as session:
            po = PoiPo()
            po.uuid = uuid
            po.name = name
            po.lat = lat
            po.long = long
            po.ssid = ssid
            po.text_content = text_content
            po.img_list = img_list
            po.created_at = datetime.now()
            po.modified_at = datetime.now()
            session.add(po)
            await session.commit()
        return uuid

    async def get_w_uuid(self, uuid: str) -> PoiPo:
        async with self.__session_maker() as session:
            return session.query(PoiPo).filter(PoiPo.uuid == uuid).first()

    async def update(self, uuid: str, po: PoiPo):
        async with self.__session_maker() as session:
            session.query(PoiPo).filter(PoiPo.uuid == uuid).update({
                'name': po.name,
                'lat': po.lat,
                'long': po.long,
                'ssid': po.ssid,
                'text_content': po.text_content,
                'img_list': po.img_list,
                'modified_at': datetime.now(),
            })
            await session.commit()


poi_dao: PoiDao = PoiDao()
