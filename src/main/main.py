# from src.main.extract.fetch_data import fetch_all
# from src.main.transform.clean_data import clean_all_stocks
# from src.main.load.load_to_postgres import load_to_postgres
# from src.main.transform.calculate_returns_volatility import process_all_tickers
from src.main.ml.forecast_volatility import process_all_tickers_garch
from src.utils.logger import setup_logger
from pathlib import Path

logger = setup_logger(__name__)

def main():
    logger.info("=== Pipeline start ===")

    project_root = Path(__file__).parent.parent.parent 
    raw_dir = project_root / 'data' / 'raw'
    clean_output = project_root / "data" / "staged" / "clean_stocks.csv"
    processed_output = project_root / "data" / "staged" / "processed_stocks.csv"
    forecast_dir = project_root / "data" / "staged" / "forecasts"

    logger.info(f"Project root: {project_root}")
    logger.info(f"Raw dir: {raw_dir}")
    logger.info(f"Clean output: {clean_output}")
    logger.info(f"Processed output: {processed_output}")
    logger.info(f"Forecast dir: {forecast_dir}")

    # fetch_all()
    # logger.info('=== Data Cleaning ===')
    # clean_all_stocks(raw_dir, clean_output)             
    # load_to_postgres()
    # logger.info('=== Calculate Returns and Volatility ===')
    # process_all_tickers(clean_output, processed_output)  
    logger.info('=== Volatility Forecast ===')
    process_all_tickers_garch(processed_output, forecast_dir) 

    logger.info("=== Pipeline end ===")

if __name__ == "__main__":
    main()