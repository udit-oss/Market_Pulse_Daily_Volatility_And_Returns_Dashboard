"""
Financial feature engineering module for stock market data.
Calculates returns, volatility, and other financial metrics.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import logging
from typing import Optional
from src.utils.logger import setup_logger


logger = setup_logger(__name__)

def calculate_financial_metrics(df: pd.DataFrame, price_col: str = 'close', window: int = 14) -> pd.DataFrame:
    """
    Calculate financial metrics for a single ticker's data.
    
    Args:
        df: DataFrame with OHLCV data for one ticker
        price_col: Column name to use for price calculations
        window: Rolling window size for volatility calculation
        
    Returns:
        DataFrame with added financial metrics
        
    Raises:
        ValueError: If required columns are missing
    """

    required_cols = ['date', price_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f'Missing required columns: {missing_cols}')
    
    if df.empty:
        raise  ValueError('Input DataFrame is empty')
    
    result_df = df.copy()

    result_df = result_df.sort_values('date').reset_index(drop=True)

    result_df['daily_return'] = np.log(result_df[price_col] / result_df[price_col].shift(1))

    # Calculate rolling volatility (annualized)
    # Standard deviation of returns over rolling window, annualized by sqrt(252 trading days)
    result_df[f'volatility_{window}d'] = result_df['daily_return'].rolling(window=window, min_periods=window).std() * np.sqrt(252)

    result_df['simple_return'] = result_df[price_col].pct_change()

    result_df['cumulative_return'] = (1 + result_df['simple_return']).cumprod() - 1

    return result_df

def process_all_tickers(input_file: Path, output_file: Path, price_col: str = 'close', window: int = 14) -> pd.DataFrame:
    """
    Process financial metrics for all tickers in a combined dataset.
    
    Args:
        input_file: Path to cleaned stock data CSV
        output_file: Path where processed data will be saved
        price_col: Column name to use for price calculations
        window: Rolling window size for volatility calculation
        
    Returns:
        Combined DataFrame with financial metrics for all tickers
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If no valid tickers found or data is malformed
    """    
    if not input_file.exists():
        raise FileNotFoundError(f'Input file not found: {input_file}')
    
    logger.info(f'Reading cleaned data from {input_file}')

    df = pd.read_csv(input_file)

    if df.empty:
        raise ValueError('Input CSV is empty')
    
    required_cols = ['ticker', 'date', price_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f'Missing required columns: {missing_cols}')
    
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    tickers = df['ticker'].unique()
    logger.info(f'Processing {len(tickers)} tickers: {list(tickers)}')

    processed_dataframes = []
    failed_tickers = []

    for ticker in tickers:
        try:
            logger.info(f'Calculating metrics for {ticker.upper()}')
            ticker_data = df[df['ticker'] == ticker].copy()

            if ticker_data.empty:
                logger.warning(f'No data found for ticker: {ticker}')
                failed_tickers.append(ticker)
                continue

            processed_ticker = calculate_financial_metrics(ticker_data, price_col=price_col, window=window)
            processed_dataframes.append(processed_ticker)

            valid_returns = processed_ticker['daily_return'].dropna()
            if len(valid_returns) > 0:
                logger.info(f'{ticker.upper()}: {len(valid_returns)} valid returns,' f'mean daily return: {valid_returns.mean():.6f}')
            else:
                logger.warning(f'{ticker.upper()}: No valid returns calculated.')
        except Exception as e:
            logger.error(f'Failed to process {ticker}: {e}')
            failed_tickers.append(ticker)
    
    if not processed_dataframes:
        raise ValueError('No valid tickers processed successfully.')
    
    logger.info(f'Combining processed data for all tickers')
    combined_df = pd.concat(processed_dataframes, ignore_index=True, sort=False)

    combined_df = combined_df.sort_values(['ticker', 'date']).reset_index(drop=True)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    combined_df.to_csv(output_file, index=False)
    
    total_rows = len(combined_df)
    successful_tickers = len(processed_dataframes)
    date_range = f'{combined_df["date"].min()} to {combined_df["date"].max()}'

    returns_na = combined_df['daily_return'].isna().sum()
    volatility_na = combined_df[f'volatility_{window}d'].isna().sum()

    logger.info('Financial metrics calculation completed')
    logger.info(f'Processed dataset: {total_rows} rows, {successful_tickers} tickers')
    logger.info(f'Date range: {date_range}')
    logger.info(f'Missing values - Daily returns: {returns_na}, Volatility: {volatility_na}')
    logger.info(f'Saved t0: {output_file}')

    if failed_tickers:
        logger.warning(f'Failed to process {len(failed_tickers)} tickers: {failed_tickers}')

    return combined_df

def validate_financial_data(df: pd.DataFrame, price_col: str = 'close') -> dict:
    """
    Validate the calculated financial metrics and return summary statistics.
    
    Args:
        df: DataFrame with calculated financial metrics
        price_col: Price column used for calculations
        
    Returns:
        Dictionary with validation results and summary statistics
    """
    validation_results = {}

    validation_results['total_rows'] = len(df)
    validation_results['unique_tickers'] = df['ticker'].nunique()
    validation_results['date_range'] = {
        'start': df['date'].min(),
        'end': df['date'].max()
    }

    returns = df['daily_return'].dropna()
    validation_results['returns'] = {
        'count': len(returns),
        'mean': returns.mean(),
        'std': returns.std(),
        'min': returns.min(),
        'max': returns.max(),
        'skewness': returns.skew(),
        'kurtosis': returns.kurtosis()
    }

    volatility_cols = [col for col in df.columns if col.startswith('volatility_')]
    if volatility_cols:
        vol_col = volatility_cols[0]
        volatility = df[vol_col].dropna()
        validation_results['volatility'] = {
            'count': len(volatility),
            'mean': volatility.mean(),
            'std': volatility.std(),
            'min': volatility.min(),
            'max': volatility.max()
        }
    
    validation_results['quality_checks'] = {
        'negative_prices': (df[price_col] <= 0).sum(),
        'missing_returns': df['daily_return'].isna().sum(),
        'infinite_returns': np.isinf(df['daily_return']).sum() if 'daily_return' in df.columns else 0,
        'extreme_returns': ((df['daily_return'].abs() > 0.5).sum()) if 'daily_return' in df.columns else 0
    }

    return validation_results

    