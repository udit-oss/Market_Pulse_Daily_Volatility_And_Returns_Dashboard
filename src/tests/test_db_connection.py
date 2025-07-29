from src.utils.db import get_engine
from src.utils.logger import setup_logger
from sqlalchemy import text

logger = setup_logger(__name__)

if __name__ == "__main__":
    engine = get_engine(echo=True)
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()
        logger.info(f"Connected to: {version}")
        print(f" DB connection OK: {version}")
