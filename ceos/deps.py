import os

from ceos.config import config
from ceos.schemas import AssetCreate


def check_if_file_exists(asset: AssetCreate):
    if not asset.file_path:
        return False
    complete_path = os.path.join(config.root_path, asset.file_path)
    return os.path.isfile(complete_path)
