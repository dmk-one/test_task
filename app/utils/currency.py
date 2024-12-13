import httpx
import json
from app.config import USD_RATE_URL
from app.redis_client import redis_client

USD_RATE_KEY = "usd_rate_rub"

def fetch_usd_rate():
    """Fetch USD rate from external API and cache it in Redis."""
    response = httpx.get(USD_RATE_URL)
    response.raise_for_status()
    data = response.json()
    rate = data["Valute"]["USD"]["Value"]
    redis_client.set(USD_RATE_KEY, rate)
    return rate

def get_usd_rate():
    """Get USD rate from Redis cache or fetch if missing."""
    rate = redis_client.get(USD_RATE_KEY)
    if rate is None:
        rate = fetch_usd_rate()
    return float(rate)
