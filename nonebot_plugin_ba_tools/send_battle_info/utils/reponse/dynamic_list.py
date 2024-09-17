from __future__ import annotations

from pydantic import BaseModel, Field


class Emoji(BaseModel):
    icon_url: str
    size: int
    text: str
    type: int


class RichTextNode(BaseModel):
    orig_text: str
    text: str
    type: str
    emoji: Emoji | None = Field(None)
    jump_url: str | None = Field(None)
    rid: str | None = Field(None)


class Desc(BaseModel):
    rich_text_nodes: list[RichTextNode]
    text: str


class Item1(BaseModel):
    height: int
    size: float
    src: str
    tags: list[str]
    width: int


class Draw(BaseModel):
    id: int
    items: list[Item1]


class Archive(BaseModel):
    aid: str
    bvid: str
    cover: str
    desc: str
    jump_url: str
    title: str
    type: int


class Major(BaseModel):
    draw: Draw | None = Field(None)
    archive: Archive | None = Field(None)
    type: str


class ModuleDynamic(BaseModel):
    desc: Desc
    major: Major | None = Field(None)


class Modules(BaseModel):
    module_dynamic: ModuleDynamic


class Item(BaseModel):
    id_str: str
    modules: Modules
    type: str
    visible: bool


class Data(BaseModel):
    has_more: bool
    items: list[Item]
    offset: str
    update_baseline: str
    update_num: int


class DynamicListResponse(BaseModel):
    code: int
    message: str
    ttl: int
    data: Data
