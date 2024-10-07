from pydantic import BaseModel


class MediaGetDto(BaseModel):
    uuid: str
    file_name: str
    content_type: str
    url: str
    file_path: str