from fastapi import HTTPException
from sqlalchemy.orm import Session

from ceos.schemas import AssetCreate, AssetPatch, AssetUpdate

from . import models, schemas


class AssetService:
    def get_assets(self, db: Session):
        assets = db.query(models.Asset).all()
        return assets

    def get_asset(self, asset_id: int, db: Session):
        return db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    def update_asset(
        self,
        db: Session,
        asset_id: int,
        asset: schemas.AssetUpdate | schemas.AssetPatch,
        partial: bool = False,
    ):
        stored_asset = self.get_asset(asset_id, db)
        if not stored_asset:
            raise HTTPException(
                status_code=404, detail="The asset with this id does not exist"
            )

        if asset.parent_asset_id == stored_asset.id:
            raise HTTPException(
                status_code=400,
                detail="parent_asset_id cannot be the same as asset id",
            )

        parent_asset = self.get_asset(asset.parent_asset_id, db)
        if not parent_asset or not parent_asset.folder:
            raise HTTPException(
                status_code=400,
                detail="parent_asset_id target is not a folder or not exist",
            )
        db.query(models.Asset).filter(models.Asset.id == stored_asset.id).update(
            asset.model_dump(exclude_none=partial)
        )
        db.commit()
        db.refresh(stored_asset)
        return stored_asset

    def create_asset(self, db: Session, asset: schemas.AssetCreate):
        if asset.parent_asset_id:
            parent_asset = self.get_asset(asset.parent_asset_id, db)
            if not parent_asset or not parent_asset.folder:
                raise HTTPException(
                    status_code=400,
                    detail="parent_asset_id target is not a folder or not exist",
                )
        db_asset = models.Asset(**asset.model_dump())
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset

    def delete_asset(self, asset_id: int, db: Session):
        asset = db.query(models.Asset).get(asset_id)
        db.delete(asset)
        db.commit()
        return asset
