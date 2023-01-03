from __future__ import annotations

from pydantic import Field, BaseModel, validator

from . import config


class Page(BaseModel):
    path: str
    url: str
    title: str
    description: str


class Account(BaseModel):
    short_name: str
    author_name: str
    author_url: str
    access_token: str
    auth_url: str


class Image(BaseModel):
    url: str = Field(..., alias="src")

    @validator("url")
    def url_validator(cls, value: str):
        return config.BASE_URL.format(endpoint=value)
