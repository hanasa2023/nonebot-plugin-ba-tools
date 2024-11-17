from __future__ import annotations

from pydantic import BaseModel, Field

# {
#         "name": "1704823962435.png",
#         "size": 5466379,
#         "is_dir": false,
#         "modified": "2024-09-23T16:21:29+08:00",
#         "created": "2024-09-23T16:21:29+08:00",
#         "sign": "G8EJ-RrotdztIefH6k2OTGSpiHeDWyXQUIuoJS0KNUs=:0",
#         "thumb": "https://thumbnail0.baidupcs.com/thumbnail/894cddc91i61ab3e29fb617e0e352276?fid=1348982596-250528-7007330552938&rt=pr&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-3HgJmvNY7zMy5U13m1x%2bbYREvMA%3d&expires=8h&chkbd=0&chkv=0&dp-logid=513618469706105102&dp-callid=0&time=1727424000&size=c850_u580&quality=100&vuk=1348982596&ft=image",
#         "type": 5,
#         "hashinfo": "null",
#         "hash_info": null
#       },


class HashInfo(BaseModel):
    md5: str


class Content(BaseModel):
    name: str
    size: int
    is_dir: bool
    modified: str
    created: str
    sign: str
    thumb: str
    type: int
    hashinfo: str
    hash_info: HashInfo | None = Field(None)


class FileInfo(BaseModel):
    name: str
    sign: str


class Illust(BaseModel):
    pid: int
    uid: int
    author: str
    title: str
    tags: list[str]
    image_url: str = Field(..., alias="imageUrl")
    ai_type: bool = Field(..., alias="aiType")
    restrict: str
