from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ceos.services import FileService

from . import crud, schemas
from .database import Base
from .main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class MockFileService:
    def check_if_file_exists(self, file_path: str | None):
        return True


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[FileService] = MockFileService

client = TestClient(app)
import contextlib

meta = Base.metadata


def create_asset(**obj):
    with TestingSessionLocal() as db:
        asset = schemas.AssetCreate(**obj)
        asset_created = crud.create_asset(db, asset)

    return asset_created


def clear_database():
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()


def test_get_assets():
    clear_database()

    response = client.get("/assets")

    assert len(response.json()) == 0

    create_asset(name="teste asset", folder=True)

    response = client.get("/assets")
    assert len(response.json()) == 1


def test_post_return_400_if_parent_id_isnt_folder():
    clear_database()

    asset_created = create_asset(name="teste asset", folder=False)

    response = client.post(
        "/assets",
        json={"name": "string", "folder": True, "parent_asset_id": asset_created.id},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "parent_asset_id target is not a folder or not exist"


def test_post_return_200_if_parent_if_is_folder():
    asset_created = create_asset(name="teste asset", folder=True)
    response = client.post(
        "/assets",
        json={"name": "string", "folder": True, "parent_asset_id": asset_created.id},
    )

    assert response.status_code == 200


def test_put_return_400_if_parent_id_isnt_folder():
    clear_database()

    asset_created = create_asset(name="teste asset", folder=False)
    asset_for_update = create_asset(name="teste asset", folder=False)

    response = client.put(
        f"/assets/{asset_for_update.id}",
        json={"name": "teste", "folder": True, "parent_asset_id": asset_created.id},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "parent_asset_id target is not a folder or not exist"


def test_put_return_200_if_parent_id_is_folder():
    clear_database()

    asset_created = create_asset(name="teste asset", folder=True)
    asset_for_update = create_asset(name="teste asset", folder=True)

    response = client.put(
        f"/assets/{asset_for_update.id}",
        json={"name": "teste", "folder": True, "parent_asset_id": asset_created.id},
    )

    assert response.status_code == 200


def test_patch_return_400_if_parent_id_isnt_folder():
    clear_database()

    asset_created = create_asset(name="teste asset", folder=False)
    asset_for_update = create_asset(name="teste asset", folder=False)

    response = client.patch(
        f"/assets/{asset_for_update.id}",
        json={"name": "teste", "parent_asset_id": asset_created.id},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "parent_asset_id target is not a folder or not exist"


def test_patch_return_200_if_parent_id_is_folder():
    clear_database()

    asset_created = create_asset(name="teste asset", folder=True)
    asset_for_update = create_asset(name="teste asset", folder=True)

    response = client.patch(
        f"/assets/{asset_for_update.id}",
        json={"name": "teste", "parent_asset_id": asset_created.id},
    )

    assert response.status_code == 200


def test_post_folder_dont_have_file_path():
    response = client.post(
        "/assets", json={"name": "string", "folder": True, "file_path": "string"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "folder cant have file_path"
