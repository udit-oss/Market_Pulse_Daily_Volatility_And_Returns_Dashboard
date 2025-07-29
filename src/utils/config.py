from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).parent.parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)


def load_config():
    """Reads environment variables from the loaded .env file.
    and returns a Python dictionary of settings"""
    return {
        "postgres": {
            "user":     os.getenv("POSTGRES_USER"),   
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host":     os.getenv("POSTGRES_HOST"),
            "port":     os.getenv("POSTGRES_PORT", "5432"),
            "db":       os.getenv("POSTGRES_DB"),
        },
        "tickers": os.getenv("TICKERS", "").split(","),
        "paths": {
            "raw_data":    os.getenv("RAW_DATA_PATH"),
            "staged_data": os.getenv("STAGED_DATA_PATH"),
        },
        "forecast_horizon": int(os.getenv("FORECAST_HORIZON", 14)),
    }
