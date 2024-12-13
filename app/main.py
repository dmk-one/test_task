from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.db import Base, engine
from app.routes import shipment_types, shipments
from app.utils.currency import fetch_usd_rate

# Создаем таблицы, если их нет
Base.metadata.create_all(bind=engine)

app = FastAPI(title="International Delivery Service")

# Настройка CORS, если нужно
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Секретный ключ для сессий
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

@app.on_event("startup")
def startup_event():
    # При старте приложения берем курс доллара и кешируем
    fetch_usd_rate()

# Подключаем роуты
app.include_router(shipment_types.router)
app.include_router(shipments.router)

@app.get("/")
def root():
    return {"detail": "Service is running"}
