from apscheduler.schedulers.background import BackgroundScheduler
from app.db import SessionLocal
from app.models import Shipment
from app.utils.currency import get_usd_rate
from app.config import DELIVERY_CALC_INTERVAL_MIN

def calculate_delivery_costs():
    """Calculate delivery costs for all shipments where cost is not calculated yet."""
    db = SessionLocal()
    try:
        usd_rate = get_usd_rate()
        shipments = db.query(Shipment).filter(Shipment.delivery_cost_rub == None).all()
        for s in shipments:
            cost = (s.weight_kg * 0.5 + s.content_value_usd * 0.01) * usd_rate
            s.delivery_cost_rub = cost
        db.commit()
    finally:
        db.close()

# Инициализация планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(calculate_delivery_costs, 'interval', minutes=DELIVERY_CALC_INTERVAL_MIN)
scheduler.start()

def run_tasks_immediately():
    # Функция для ручного запуска периодических задач
    calculate_delivery_costs()
