from sqlalchemy import Column, String, LargeBinary, DateTime

from entity.po.BasePo import BasePo

class PoiWIdentifyImagePo(BasePo):
    __tablename__ = 'poi_w_identify_image'

    poi_uuid = Column(String(255))
    image_uuid = Column(String(255))
    image_url = Column(String())
    keypoints = Column(LargeBinary)
    descriptors = Column(LargeBinary)

    created_at = Column(DateTime)
    modified_at = Column(DateTime)