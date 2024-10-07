from pydantic import BaseModel

# REQUEST DTO

class AddPoiRequestDto(BaseModel):
    name: str
    lat: float
    long: float
    ssid: str
    content: str
    img_list: str


class NearbyRequestDto(BaseModel):
    lat: float
    long: float


class MatchPoiRequestDto(BaseModel):
    poi_id: str
    image_media_id: str

class MatchLocationRequestDto(BaseModel):
    lat: float
    long: float
    ssid: str
    image_media_id: str

# RESPONSE DTO

class PoiResponseDto(BaseModel):
    uuid: str
    name: str
    lat: float
    long: float
    ssid: str
    content: str
    img_list: str