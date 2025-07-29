import pandas as pd
from pathlib import Path
from sqlalchemy import text
from src.utils.config import load_config
from src.utils.db import get_engine
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def load_to_postgres():
    cfg     = load_config()
    raw_dir = Path(cfg["paths"]["raw_data"])
    engine  = get_engine(echo=False)
    table   = "marketpulse.stg_stocks"

    logger.info(f"Truncating table {table}")
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table};"))

    csv_files = list(raw_dir.glob("*.csv"))
    if not csv_files:
        logger.warning(f"No CSV files found in {raw_dir}")
        return

    expected = ["ticker","date","open","high","low","close","volume"]

    for csv_path in csv_files:
        try:
            logger.info(f"Reading {csv_path.name}")
            df = pd.read_csv(csv_path)

            df.columns = [c.strip().lower() for c in df.columns]

            missing_cols = set(expected) - set(df.columns)
            if missing_cols:
                logger.error(f"Missing columns in {csv_path.name}: {missing_cols}")
                continue

            df = df[expected]

            df["date"] = pd.to_datetime(df["date"])
            df["ticker"] = df["ticker"].astype(str)
           
            numeric_cols = ["open", "high", "low", "close", "volume"]
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            before = len(df)
            df.dropna(how="all", inplace=True)
            dropped = before - len(df)
            if dropped:
                logger.info(f"Dropped {dropped} empty rows from {csv_path.name}")

            logger.info(f"DataFrame dtypes: {df.dtypes.to_dict()}")
            logger.info(f"Sample data: {df.head(1).to_dict('records')}")

            df.to_sql(
                name="stg_stocks",
                schema="marketpulse",
                con=engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000
            )
            logger.info(f"Loaded {len(df)} rows from {csv_path.name}")

        except Exception as e:
            logger.error(f"Failed loading {csv_path.name}: {e}", exc_info=True)
            if 'df' in locals():
                logger.error(f"DataFrame shape: {df.shape}")
                logger.error(f"DataFrame columns: {list(df.columns)}")
                logger.error(f"DataFrame dtypes: {df.dtypes.to_dict()}")

if __name__ == "__main__":
    load_to_postgres()