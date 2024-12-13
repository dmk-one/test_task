from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class ShipmentType(Base):
    __tablename__ = "shipment_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Пример типов: "clothes", "electronics", "misc"

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    user_session_id = Column(String(255), index=True)  # привязка к сессии
    name = Column(String(100), nullable=False)
    weight_kg = Column(Float, nullable=False)
    content_value_usd = Column(Float, nullable=False)
    shipment_type_id = Column(Integer, ForeignKey("shipment_types.id"), nullable=False)
    delivery_cost_rub = Column(Float, nullable=True)  # если рассчитано

    shipment_type = relationship("ShipmentType", backref="shipments")
