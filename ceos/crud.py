from sqlalchemy.orm import Session

from . import models, schemas


def get_assets(db: Session):
    assets = db.query(models.Asset).all()
    return assets


def get_asset(asset_id: int, db: Session):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()


def update_asset(
    db: Session, stored_asset: models.Asset, new_asset_content: schemas.AssetUpdate | schemas.AssetPatch
):
    db.query(models.Asset).filter(models.Asset.id == stored_asset.id).update(
        new_asset_content.model_dump(exclude_none=True)
    )
    db.commit()
    db.refresh(stored_asset)
    return stored_asset


def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def delete_asset(asset_id: int, db: Session):
    asset = db.query(models.Asset).get(asset_id)
    db.delete(asset)
    db.commit()
    return asset
