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


class AssetCreate(AssetBase):
    pass


class AssetUpdate(AssetBase):
    pass


class AssetPatch(AssetBase):
    name: str | None = None
    parent_asset_id: int | None = None

    @field_validator("parent_asset_id")
    @classmethod
    def parent_asset_id_must_be_bigger_than_zero(cls, v: int):
        if v is not None and v <= 0:
            raise ValueError("Parent asset id must be bigger than zero")
        return v


class Asset(AssetBase):
    id: int
    child_assets: list[Asset] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
