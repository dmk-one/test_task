import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/shipments_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
USD_RATE_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
DELIVERY_CALC_INTERVAL_MIN = 5  # интервал в минутах для периодической задачи

# Настройки пагинации по умолчанию
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50
