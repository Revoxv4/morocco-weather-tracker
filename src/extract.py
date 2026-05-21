"""Extract weather data from OpenWeatherMap API and persist to bronze layer."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Project root is two levels up from this file (src/extract.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def get_weather(city: str) -> dict[str, Any]:
    """Fetch current weather for a city from OpenWeatherMap.

    Args:
        city: City name (e.g., "Casablanca").

    Returns:
        Dictionary with weather data from the API.

    Raises:
        ValueError: If API key is missing.
        requests.HTTPError: If the API request fails.
    """
    if not API_KEY:
        raise ValueError(
            "OPENWEATHER_API_KEY not found. Check your .env file."
        )

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def save_raw_response(city: str, data: dict[str, Any]) -> Path:
    """Save raw API response to bronze layer with timestamped filename.

    File naming: data/raw/<city_lowercase>_<UTC_timestamp>.json
    Example: data/raw/casablanca_2026-05-21T14-30-00Z.json

    Args:
        city: City name used in the filename.
        data: API response dictionary to save.

    Returns:
        Path to the saved file.
    """
    # Ensure directory exists (idempotent — safe to call repeatedly)
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # UTC timestamp; colons replaced with dashes (illegal in some filesystems)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    city_slug = city.lower().replace(" ", "_")
    filename = f"{city_slug}_{timestamp}.json"
    filepath = RAW_DATA_DIR / filename

    # Add ingestion metadata (the "envelope" pattern — pros do this)
    payload = {
        "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "openweathermap",
        "city_query": city,
        "data": data,
    }

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return filepath


if __name__ == "__main__":
    city = "Casablanca"
    data = get_weather(city)
    saved_path = save_raw_response(city, data)

    # Quick summary print
    print(f"✓ Extracted weather for {city}")
    print(f"  Temperature: {data['main']['temp']}°C")
    print(f"  Conditions:  {data['weather'][0]['description']}")
    print(f"  Saved to:    {saved_path.relative_to(PROJECT_ROOT)}")