from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ceos import crud, schemas
from ceos.services import UserService

from .database import SessionLocal

app = FastAPI()

# TODO: create a allow origins config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/assets/", response_model=list[schemas.Asset])
def read_assets(db: Session = Depends(get_db)):
    return crud.get_assets(db)


@app.get("/assets/{asset_id}", response_model=schemas.Asset)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(asset_id, db)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@app.post("/assets/", response_model=schemas.Asset)
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(UserService),
):
    user_service.validate_create(asset)
    user_service.validate_parent_asset(asset.parent_asset_id, crud, db)
    return crud.create_asset(db, asset)


@app.put("/assets/{asset_id}", response_model=schemas.Asset)
def update_asset(
    asset: schemas.AssetUpdate,
    asset_id: int,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(UserService),
):
    user_service.validate_update(asset)
    stored_asset = crud.get_asset(asset_id, db)
    if not stored_asset:
        raise HTTPException(
            status_code=404, detail="The asset with this id does not exist"
        )
    user_service.validate_parent_asset(asset.parent_asset_id, crud, db)
    return crud.update_asset(db, stored_asset, asset)


@app.patch("/assets/{asset_id}", response_model=schemas.Asset)
def partial_update_asset(
    asset: schemas.AssetPatch,
    asset_id: int,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(UserService),
):
    stored_asset = crud.get_asset(asset_id, db)
    if not stored_asset:
        raise HTTPException(
            status_code=404, detail="The asset with this id does not exist"
        )

    user_service.validate_parent_asset(asset.parent_asset_id, crud, db)
    return crud.update_asset(db, stored_asset, asset)


@app.delete("/assets/{asset_id}", response_model=schemas.Asset)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(asset_id, db)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return crud.delete_asset(asset_id, db)
