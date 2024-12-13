from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import ShipmentType
from app.schemas import ShipmentTypeResponse

router = APIRouter()

@router.get("/shipment_types", response_model=list[ShipmentTypeResponse])
def get_shipment_types(db: Session = Depends(get_db)):
    """Get all shipment types"""
    types = db.query(ShipmentType).all()
    return types
