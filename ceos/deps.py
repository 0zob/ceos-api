import os

from ceos.config import config
from ceos.schemas import AssetCreate
from ceos.services import UserService


def check_if_file_exists(file_path: str):
    if not file_path:
        return False
    complete_path = os.path.join(config.root_path, file_path)
    return os.path.isfile(complete_path)

user_service = UserService(check_if_file_exists)
