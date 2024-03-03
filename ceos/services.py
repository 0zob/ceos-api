from fastapi import HTTPException
from ceos.config import config
import os

from ceos.schemas import AssetCreate, AssetUpdate


class FileService:
    def check_if_file_exists(self,file_path: str | None):
        if not file_path:
            return False
        complete_path = os.path.join(config.root_path, file_path)
        return os.path.isfile(complete_path)
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
