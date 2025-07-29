from extract.fetch_data import fetch_all
from load.load_to_postgres import load_to_postgres
from utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    logger.info("=== Day 1 pipeline start ===")
    fetch_all()             
    load_to_postgres()     
    logger.info("=== Day 1 pipeline end ===")

if __name__ == "__main__":
    main()