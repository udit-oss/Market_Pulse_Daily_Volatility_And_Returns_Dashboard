"""
Data cleaning module for stock market data.
Converts raw csv files to cleaned standardized format.
"""

import pandas as pd
from pathlib import Path
import logging
from typing import List, Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def clean_stock_data(csv_path: Path) -> pd.DataFrame:
    """
    Clean a single stock CSV file.
    
    Args:
        csv_path: Path to the raw CSV file
        
    Returns:
        Cleaned DataFrame with standardized columns and data types
        
    Raises:
        ValueError: If file doesn't contain expected columns
        FileNotFoundError: If CSV file doesn't exist
    """

    if not csv_path.exists():
        raise FileNotFoundError(f'CSV file not found: {csv_path}')
    
    logger.info(f'Cleaning {csv_path.name}')

    df = pd.read_csv(csv_path)
    original_rows = len(df)

    expected_cols = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f'Missing expected columns in {csv_path.name}: {missing_cols}')
    
    df = df.dropna(subset=expected_cols)

    price_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in price_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        logger.error(f'Failed to convert date column in {csv_path.name}: {e}')
        raise ValueError(f'Invalid date format in {csv_path.name}')

    df = df.dropna()

    df = df.sort_values('date').reset_index(drop=True)

    final_rows = len(df)
    dropped = original_rows - final_rows

    if dropped > 0:
        drop_pct = (dropped / original_rows) * 100
        logger.warning(f'{csv_path.name}: Dropped {dropped}/{original_rows} rows ({drop_pct:.1f}%)')

        if drop_pct > 10:
            logger.error(f'High data loss in {csv_path.name}: {drop_pct:.1f}% - check data quality')

    logger.info(f'Cleaned {csv_path.name}: {final_rows} rows, date range {df['date'].min()} to {df['date'].max()}')
    return df

def clean_all_stocks(input_dir: Path, output_file: Path) -> pd.DataFrame:
    """
    Clean all stock CSV files and combine into a single dataset.
    
    Args:
        input_dir: Directory containing raw CSV files
        output_file: Path where combined cleaned data will be saved
        
    Returns:
        Combined DataFrame with all cleaned stock data
        
    Raises:
        FileNotFoundError: If input directory doesn't exist
        ValueError: If no valid CSV files found
    """

    if not input_dir.exists():
        raise FileNotFoundError(f'Input directory not found: {input_dir}')
    
    csv_files = list(input_dir.glob('*.csv'))

    if not csv_files:
        raise ValueError(f'No CSV files found in {input_dir}')
    
    logger.info(f'Found {len(csv_files)} CSV files in {input_dir}')

    cleaned_dataframes = []
    failed_files = []

    for csv_path in sorted(csv_files):
        try:
            cleaned_df = clean_stock_data(csv_path)
            if not cleaned_df.empty:
                cleaned_dataframes.append(cleaned_df)
            else:
                logger.warning(f'No valid data after cleaning: {csv_path.name}')
                failed_files.append(csv_path.name)
        except Exception as e:
            logger.error(f'Failed to clean {csv_path.name}: {e}')
            failed_files.append(csv_path.name)

    if not cleaned_dataframes:
        raise ValueError('No files could be successfully cleaned.')
    
    combined_df = pd.concat(cleaned_dataframes, ignore_index=True, sort=False)

    combined_df = combined_df.sort_values(['ticker', 'date']).reset_index(drop=True)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    combined_df.to_csv(output_file, index=False)

    total_rows = len(combined_df)
    unique_tickers = combined_df['ticker'].nunique()
    date_range = f'{combined_df["date"].min()} to {combined_df["date"].max()}'

    logger.info(f'Cleaning completed successfully')
    logger.info(f'Combined dataset: {total_rows} rows, {unique_tickers} tickers')
    logger.info(f'Date range: {date_range}')
    logger.info(f'Saved to: {output_file}')

    if failed_files:
        logger.warning(f'Failed to clean {len(failed_files)} files: {failed_files}')

    return combined_df