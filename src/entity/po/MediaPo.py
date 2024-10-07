from enum import Enum

from sqlalchemy import Column, String, Float, DateTime, Integer

from entity.po.BasePo import BasePo


class MediaPo(BasePo):
    __tablename__ = 'media'

    uuid = Column(String(255))
    file_name = Column(String(255))
    content_type = Column(String)
    url = Column(String)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
