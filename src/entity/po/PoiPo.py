from sqlalchemy import Column, String, Float, DateTime

from entity.po.BasePo import BasePo


class PoiPo(BasePo):
    __tablename__ = 'poi'

    uuid = Column(String(255))
    name = Column(String(255))
    thumbnail = Column(String)
    lat = Column(Float)
    long = Column(Float)
    content = Column(String)
    identify_image = Column(String)

    created_at = Column(DateTime)
    modified_at = Column(DateTime)