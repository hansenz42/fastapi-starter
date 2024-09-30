from enum import Enum

from sqlalchemy import Column, String, Float, DateTime, Integer

from entity.po.BasePo import BasePo


class FileTypeEnum(Enum):
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3


class MediaPo(BasePo):
    __tablename__ = 'media'

    uuid = Column(String(255))
    file_name = Column(String(255))
    file_type = Column(Integer)
    url = Column(String)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
