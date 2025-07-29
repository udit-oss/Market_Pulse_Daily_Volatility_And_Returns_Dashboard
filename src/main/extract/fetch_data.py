import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from src.utils.config import load_config
from src.utils.logger import setup_logger

logger   = setup_logger(__name__)
cfg      = load_config()
tickers  = cfg["tickers"]
raw_dir  = Path(cfg["paths"]["raw_data"])
raw_dir.mkdir(parents=True, exist_ok=True)

end   = datetime.today()
start = end - timedelta(days=365)

success, failed = 0, 0

for t in tickers:
    ticker = t.lower()
    try:
        logger.info(f"Fetching data for {ticker}")
        df = yf.download(t, start=start, end=end, progress=False)
        if df.empty:
            logger.warning(f"No data returned for {ticker}")
            failed += 1
            continue

        df.reset_index(inplace=True)
        df = df.rename(columns={
            "Date": "date", "Open": "open", "High": "high",
            "Low": "low", "Close": "close", "Volume": "volume"
        })
        df["ticker"] = ticker
        df = df[["ticker", "date", "open", "high", "low", "close", "volume"]]

        temp_path = raw_dir / f"{ticker}.csv.tmp"
        out_path  = raw_dir / f"{ticker}.csv"
        df.to_csv(temp_path, index=False)
        temp_path.rename(out_path)

        logger.info(f"Saved {len(df)} rows to {out_path}")
        success += 1

    except Exception as e:
        logger.error(f"Failed to fetch {ticker}: {e}", exc_info=True)
        failed += 1

logger.info(f"Fetch complete: {success} succeeded, {failed} failed.")