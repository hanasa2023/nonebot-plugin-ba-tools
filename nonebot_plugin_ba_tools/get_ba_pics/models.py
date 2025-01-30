from __future__ import annotations

from pydantic import BaseModel, Field


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


class MemeInfo(BaseModel):
    name: str
    url: str
    hash: str


class Illust(BaseModel):
    pid: int
    uid: int
    author: str
    title: str
    tags: list[str]
    image_url: str = Field(..., alias="imageUrl")
    ai_type: bool = Field(..., alias="aiType")
    restrict: str
    love_members: int = Field(..., alias="loveMembers")
    hate_memebers: int = Field(..., alias="hateMembers")
