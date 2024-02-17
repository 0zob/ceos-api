from datetime import datetime
from typing import ForwardRef

from pydantic import BaseModel

Asset = ForwardRef("Asset")


class AssetBase(BaseModel):
    name: str
    parent_asset_id: int | None = None
    folder: bool = False


class AssetCreate(AssetBase):
    pass


class Asset(AssetBase):
    id: int
    child_assets: list[Asset] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
