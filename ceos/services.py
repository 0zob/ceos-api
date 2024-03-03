import os

from fastapi import Depends, HTTPException

from ceos.config import config
from ceos.schemas import AssetCreate, AssetPatch, AssetUpdate


class FileService:
    def check_if_file_exists(self, file_path: str | None):
        if not file_path:
            return False
        complete_path = os.path.join(config.root_path, file_path)
        return os.path.isfile(complete_path)


class UserService:
    def __init__(self, file_service: FileService = Depends(FileService)) -> None:
        self._file_service = file_service

    def validate_create(self, asset: AssetCreate):
        if asset.folder and asset.file_path is not None:
            raise HTTPException(detail="folder cant have file_path", status_code=400)
        if not asset.folder and not self._file_service.check_if_file_exists(
            asset.file_path
        ):
            raise HTTPException(detail="file_path target not found", status_code=404)

    def validate_update(self, asset: AssetUpdate):
        if asset.folder and asset.file_path is not None:
            raise HTTPException(detail="Folder cant have file_path", status_code=400)
        if not asset.folder and not self._file_service.check_if_file_exists(
            asset.file_path
        ):
            raise HTTPException(detail="file_path target not found", status_code=404)

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
