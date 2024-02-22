from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ceos import crud, schemas

from .database import SessionLocal

app = FastAPI()

#TODO: create a allow origins config
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
    return crud.get_asset(asset_id, db)


@app.post("/assets/", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    if asset.parent_asset_id:
        parent_asset = crud.get_asset(asset.parent_asset_id, db)
        if not parent_asset or not parent_asset.folder:
            raise HTTPException(
                status_code=400,
                detail="parent_asset_id target is not a folder or not exist",
            )
    return crud.create_asset(db, asset)


@app.put("/assets/{asset_id}", response_model=schemas.Asset)
def update_asset(
    asset: schemas.AssetUpdate, asset_id: int, db: Session = Depends(get_db)
):
    stored_asset = crud.get_asset(asset_id, db)
    if not stored_asset:
        raise HTTPException(
            status_code=404, detail="The asset with this id does not exist"
        )
    if asset.parent_asset_id:
        parent_asset = crud.get_asset(asset.parent_asset_id, db)
        if not parent_asset or not parent_asset.folder:
            raise HTTPException(
                status_code=400,
                detail="parent_asset_id target is not a folder or not exist",
            )
    return crud.update_asset(db, stored_asset, asset)
