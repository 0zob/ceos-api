from datetime import datetime
from typing import ForwardRef

from pydantic import BaseModel, field_validator

Asset = ForwardRef("Asset")


class AssetBase(BaseModel):
    name: str
    parent_asset_id: int | None = None
    folder: bool = False
    file_path: str | None = None

    @field_validator("parent_asset_id")
    @classmethod
    def parent_asset_id_must_be_bigger_than_zero(cls, v: int):
        if v is not None and v <= 0:
            raise ValueError("Parent asset id must be bigger than zero")
        return v

    @field_validator("file_path")
    @classmethod
    def file_path_cant_be_empty_for_files(cls, v: str, values):
        folder = values.data.get("folder")
        if v == "" and folder == False:
            raise ValueError("file_path cant be empty for files")
        return v

    @field_validator("file_path")
    @classmethod
    def folder_asset_dont_have_file_path(cls, v: str, values):
        folder = values.data.get("folder")
        if folder and v:
            raise ValueError("Folders dont have file path")
        return v


class AssetCreate(AssetBase):
    pass


class AssetUpdate(AssetBase):
    pass


class Asset(AssetBase):
    id: int
    child_assets: list[Asset] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
