import os

from fastapi import Depends, HTTPException

from ceos.config import config
from ceos.schemas import AssetCreate, AssetPatch, AssetUpdate


class UserService:
    def validate_parent_asset(self, asset: AssetCreate, crud, db):
        if not asset.parent_asset_id:
            return
        parent_asset = crud.get_asset(asset.parent_asset_id, db)
        if not parent_asset or not parent_asset.folder:
            raise HTTPException(
                status_code=400,
                detail="parent_asset_id target is not a folder or not exist",
            )

    def validate_parent_asset_for_update(
        self, asset: AssetUpdate | AssetPatch, asset_id: int, crud, db
    ):
        stored_asset = crud.get_asset(asset_id, db)
        if not stored_asset:
            raise HTTPException(
                status_code=404, detail="The asset with this id does not exist"
            )

        if not asset.parent_asset_id:
            return stored_asset

        if asset.parent_asset_id == asset_id:
            raise HTTPException(
                status_code=400,
                detail="parent_asset_id cannot be the same as asset id",
            )

        parent_asset = crud.get_asset(asset.parent_asset_id, db)
        if not parent_asset or not parent_asset.folder:
            raise HTTPException(
                status_code=400,
                detail="parent_asset_id target is not a folder or not exist",
            )
        return stored_asset
