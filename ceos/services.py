from fastapi import HTTPException

from ceos.schemas import AssetCreate, AssetUpdate


class UserService:
    def __init__(self, check_if_file_exists) -> None:
        self._file_exists = check_if_file_exists

    def validate_create(self, asset: AssetCreate):
        if asset.folder and asset.file_path is not None:
            raise HTTPException(detail="Folder cant have file_path", status_code=400)
        if not asset.folder and not self._file_exists(asset.file_path):
            raise HTTPException(detail="file_path target not found", status_code=404)

    def validate_update(self, asset: AssetUpdate):
        if asset.folder and asset.file_path is not None:
            raise HTTPException(detail="Folder cant have file_path", status_code=400)
        if not asset.folder and not self._file_exists(asset.file_path):
            raise HTTPException(detail="file_path target not found", status_code=404)
