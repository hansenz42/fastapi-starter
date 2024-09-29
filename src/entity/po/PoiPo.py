from sqlalchemy import Column, String, Float, DateTime

from entity.po.BasePo import BasePo


class PoiPo(BasePo):
    __tablename__ = 'poi'

    uuid = Column(String(255))
    name = Column(String(255))
    thumbnail = Column(String)
    lat = Column(Float)
    long = Column(Float)
    ssid = Column(String(255))
    text_content = Column(String)
    img_list = Column(String)

    created_at = Column(DateTime)
    modified_at = Column(DateTime)