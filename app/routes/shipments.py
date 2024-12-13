from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.models import Shipment, ShipmentType
from app.schemas import ShipmentCreate, ShipmentResponse, ShipmentFilterParams
from app.utils.pagination import paginate_query
from app.utils.exceptions import NotFoundError
from sqlalchemy import and_

router = APIRouter()

@router.post("/shipments", response_model=int)
def register_shipment(shipment: ShipmentCreate, request: Request, db: Session = Depends(get_db)):
    """
    Register a new shipment. Returns the shipment's ID.
    Shipment is tied to the user session.
    """
    # Проверяем тип посылки
    st = db.query(ShipmentType).filter(ShipmentType.id == shipment.shipment_type_id).first()
    if not st:
        raise NotFoundError(detail="Shipment type not found")

    session_id = request.session.get("user_session_id")
    if not session_id:
        # Если нет сессии - генерируем новую
        session_id = request.cookies.get("session_id")
        if not session_id:
            # Генерируем новую сессию
            import uuid
            session_id = str(uuid.uuid4())
        request.session["user_session_id"] = session_id

    new_shipment = Shipment(
        user_session_id=session_id,
        name=shipment.name,
        weight_kg=shipment.weight_kg,
        content_value_usd=shipment.content_value_usd,
        shipment_type_id=shipment.shipment_type_id
    )
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    return new_shipment.id

@router.get("/shipments", response_model=List[ShipmentResponse])
def list_shipments(filter_params: ShipmentFilterParams = Depends(), request: Request = None, db: Session = Depends(get_db)):
    """
    Get list of shipments for current session with optional filters and pagination.
    Filters:
      - shipment_type_id: int
      - delivery_computed: bool
    """
    session_id = request.session.get("user_session_id")
    if not session_id:
        return []

    query = db.query(Shipment).join(ShipmentType).filter(Shipment.user_session_id == session_id)

    if filter_params.shipment_type_id is not None:
        query = query.filter(Shipment.shipment_type_id == filter_params.shipment_type_id)
    if filter_params.delivery_computed is not None:
        if filter_params.delivery_computed:
            query = query.filter(Shipment.delivery_cost_rub != None)
        else:
            query = query.filter(Shipment.delivery_cost_rub == None)

    query = paginate_query(query, filter_params.page, filter_params.page_size)
    shipments = query.all()

    result = []
    for sh in shipments:
        result.append(
            ShipmentResponse(
                id=sh.id,
                name=sh.name,
                weight_kg=sh.weight_kg,
                content_value_usd=sh.content_value_usd,
                shipment_type_name=sh.shipment_type.name,
                delivery_cost_rub=sh.delivery_cost_rub if sh.delivery_cost_rub else None
            )
        )

    return result

@router.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(shipment_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Get shipment by ID for current user session.
    """
    session_id = request.session.get("user_session_id")
    if not session_id:
        raise NotFoundError(detail="No shipments for this session")

    sh = db.query(Shipment).join(ShipmentType).filter(
        Shipment.id == shipment_id,
        Shipment.user_session_id == session_id
    ).first()

    if not sh:
        raise NotFoundError(detail="Shipment not found")

    return ShipmentResponse(
        id=sh.id,
        name=sh.name,
        weight_kg=sh.weight_kg,
        content_value_usd=sh.content_value_usd,
        shipment_type_name=sh.shipment_type.name,
        delivery_cost_rub=sh.delivery_cost_rub if sh.delivery_cost_rub else None
    )

@router.post("/shipments/run_tasks")
def run_tasks_manually():
    """Endpoint for running periodic tasks manually for debugging."""
    from app.utils.tasks import run_tasks_immediately
    run_tasks_immediately()
    return {"detail": "Tasks executed"}
