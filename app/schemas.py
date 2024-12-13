from pydantic import BaseModel, Field
from typing import Optional, List


class ShipmentCreate(BaseModel):
    name: str = Field(..., max_length=100)
    weight_kg: float = Field(..., gt=0)
    content_value_usd: float = Field(..., gt=0)
    shipment_type_id: int

class ShipmentResponse(BaseModel):
    id: int
    name: str
    weight_kg: float
    content_value_usd: float
    shipment_type_name: str
    delivery_cost_rub: Optional[float] = None

    class Config:
        orm_mode = True

class ShipmentTypeResponse(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

# Параметры для фильтрации и пагинации
class ShipmentFilterParams(BaseModel):
    shipment_type_id: Optional[int] = None
    delivery_computed: Optional[bool] = None
    page: int = 1
    page_size: int = 10
