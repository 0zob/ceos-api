from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ceos import schemas
from ceos.services import AssetService

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
def read_assets(
    db: Session = Depends(get_db),
    asset_service: AssetService = Depends(AssetService),
):
    return asset_service.get_assets(db)


@app.get("/assets/{asset_id}", response_model=schemas.Asset)
def read_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    asset_service: AssetService = Depends(AssetService),
):
    asset = asset_service.get_asset(asset_id, db)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@app.post("/assets/", response_model=schemas.Asset)
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
    asset_service: AssetService = Depends(AssetService),
):
    return asset_service.create_asset(db, asset)


@app.put("/assets/{asset_id}", response_model=schemas.Asset)
def update_asset(
    asset: schemas.AssetUpdate,
    asset_id: int,
    db: Session = Depends(get_db),
    asset_service: AssetService = Depends(AssetService),
):
    return asset_service.update_asset(db, asset_id, asset)


@app.patch("/assets/{asset_id}", response_model=schemas.Asset)
def partial_update_asset(
    asset: schemas.AssetPatch,
    asset_id: int,
    db: Session = Depends(get_db),
    asset_service: AssetService = Depends(AssetService),
):
    return asset_service.update_asset(db, asset_id, asset, partial=True)


@app.delete("/assets/{asset_id}", response_model=schemas.Asset)
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    asset_service: AssetService = Depends(AssetService),
):
    asset = asset_service.get_asset(asset_id, db)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset_service.delete_asset(asset_id, db)
