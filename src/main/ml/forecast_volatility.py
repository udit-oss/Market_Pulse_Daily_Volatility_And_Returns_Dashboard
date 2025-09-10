"""
GARCH volatility forecasting module for stock market data.
Fits GARCH(1,1) models and generates volatility forecasts.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Tuple
import warnings
from src.utils.logger import setup_logger
warnings.filterwarnings('ignore')

logger = setup_logger(__name__)

try:
    from arch import arch_model
    logger.info('ARCH library found')
except ImportError:
    logger.error('ARCH library not found - install with: pip install arch')
    raise ImportError("ARCH library required for GARCH modeling")

def fit_garch_model(returns: pd.Series, ticker: str, dist: 'str' = 'normal') -> Optional[dict]:
    """
    Fit GARCH(1,1) model to return series.
    
    Args:
        returns: Daily return series (must be stationary)
        ticker: Stock ticker for logging
        dist: Error distribution ('normal' or 't' for Student-t)
        
    Returns:
        Dictionary with model results or None if fitting failed
        
    Raises:
        ValueError: If returns series is invalid
    """
    if returns.empty:
        raise ValueError(f'Empty returns series for {ticker}')
    
    clean_returns = returns.dropna() * 100

    if len(clean_returns) < 50:
        logger.warning(f'{ticker}: Insufficient data for GARCH fitting ({len(clean_returns)} observations)')
        return None
    
    try:
        model = arch_model(clean_returns, vol='Garch', p=1, q=1, dist=dist)
        fitted_model = model.fit(disp='off')
        
        params = fitted_model.params
        
        forecasts = fitted_model.forecast(horizon=5)
        forecasted_vols = forecasts.variance.iloc[-1].values ** 0.5 / 100
        
        results = {
            'ticker': ticker,
            'model': fitted_model,
            'aic': fitted_model.aic,
            'bic': fitted_model.bic,
            'loglikelihood': fitted_model.loglikelihood,
            'omega': params.get('omega', np.nan),
            'alpha': params.get('alpha[1]', np.nan),
            'beta': params.get('beta[1]', np.nan),
            'persistence': params.get('alpha[1]', 0) + params.get('beta[1]', 0),
            'conditional_volatility': fitted_model.conditional_volatility,
            'returns_used': clean_returns,
            'n_observations': len(clean_returns)
        }

        logger.info(f'{ticker.upper()}: AIC={fitted_model.aic:.2f}, 'f'Persistence={results["persistence"]:.4f}')
        
        return results
    
    except Exception as e:
        logger.error(f'GARCH fitting failed for {ticker}: {e}')
        return None
    
def generate_volatility_forecasts(garch_results: Dict, horizon: int = 14) -> pd.DataFrame:
    """
    Generate volatility forecasts using fitted GARCH model.
    
    Args:
        garch_results: Dictionary from fit_garch_model()
        horizon: Number of days ahead to forecast
        
    Returns:
        DataFrame with forecast dates and volatility predictions
        
    Raises:
        ValueError: If garch_results is invalid
    """
    if not garch_results or 'model' not in garch_results:
        raise ValueError('Invalid GARCH results provided')
    
    model = garch_results['model']
    ticker = garch_results['ticker']

    try:
        logger.info(f'Generating {horizon}-day volatility forecast for {ticker.upper()}')

        forecast = model.forecast(horizon=horizon, method='simulation', simulations=1000)

        forecast_variance = forecast.variance.iloc[-1]
        forecast_volatility = np.sqrt(forecast_variance)

        last_date = pd.Timestamp.today()
        forecast_dates = pd.bdate_range(start=last_date + pd.Timedelta(days=1), periods=horizon, freq='B')

        forecast_df = pd.DataFrame({
            'ticker': ticker,
            'forecast_date': forecast_dates,
            'forecast_volatility': forecast_volatility.values,
            'forecast_variance': forecast_variance.values,
            'forecast_horizon': np.arange(1, horizon + 1)
        })

        logger.info(f"{ticker.upper()}: Generated {len(forecast_df)} day forecast, "
                   f"avg volatility {forecast_df['forecast_volatility'].mean():.4f}%")
        
        return forecast_df
    
    except Exception as e:
        logger.error(f"Forecast generation failed for {ticker}: {e}")
        return pd.DataFrame()

def process_all_tickers_garch(input_file: Path, output_dir: Path, 
                             forecast_horizon: int = 14) -> Dict[str, Dict]:
    """
    Fit GARCH models and generate forecasts for all tickers.
    
    Args:
        input_file: Path to processed stock data CSV
        output_dir: Directory where forecast files will be saved
        forecast_horizon: Number of days ahead to forecast
        
    Returns:
        Dictionary with GARCH results for each ticker
        
    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    logger.info(f"Starting GARCH analysis from {input_file}")
    
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    
    tickers = df['ticker'].unique()
    logger.info(f"Processing GARCH models for {len(tickers)} tickers: {list(tickers)}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_results = {}
    all_forecasts = []
    
    for ticker in tickers:
        try:
            ticker_data = df[df['ticker'] == ticker].sort_values('date')
            returns = ticker_data['daily_return']
            
            garch_results = fit_garch_model(returns, ticker, dist='normal')
            
            if garch_results is None:
                logger.warning(f"Skipping forecast for {ticker} due to fitting failure")
                continue
            
            all_results[ticker] = garch_results
            
            forecast_df = generate_volatility_forecasts(garch_results, forecast_horizon)
            
            if not forecast_df.empty:
                forecast_file = output_dir / f"{ticker}_garch_forecast.csv"
                forecast_df.to_csv(forecast_file, index=False)
                logger.info(f"Saved forecast: {forecast_file}")
                
                all_forecasts.append(forecast_df)
            
        except Exception as e:
            logger.error(f"Failed to process {ticker}: {e}")
            continue
    
    if all_forecasts:
        combined_forecasts = pd.concat(all_forecasts, ignore_index=True)
        combined_file = output_dir / "all_tickers_garch_forecasts.csv"
        combined_forecasts.to_csv(combined_file, index=False)
        logger.info(f"Saved combined forecasts: {combined_file}")
    
    if all_results:
        comparison_data = []
        for ticker, results in all_results.items():
            comparison_data.append({
                'ticker': ticker.upper(),
                'aic': results['aic'],
                'bic': results['bic'],
                'loglikelihood': results['loglikelihood'],
                'omega': results['omega'],
                'alpha': results['alpha'],
                'beta': results['beta'],
                'persistence': results['persistence'],
                'observations': results['n_observations']
            })
        
        comparison_df = pd.DataFrame(comparison_data).sort_values('aic')
        summary_file = output_dir / "garch_model_comparison.csv"
        comparison_df.to_csv(summary_file, index=False)
        logger.info(f"Saved model comparison: {summary_file}")
        
        logger.info("GARCH Model Summary:")
        for _, row in comparison_df.iterrows():
            logger.info(f"{row['ticker']}: AIC={row['aic']:.2f}, "
                       f"Persistence={row['persistence']:.4f}")
    
    logger.info(f"GARCH analysis completed: {len(all_results)} models fitted")
    return all_results


def validate_garch_results(garch_results: Dict) -> Dict[str, Dict]:
    """
    Validate GARCH model results and identify potential issues.
    
    Args:
        garch_results: Dictionary of GARCH results from process_all_tickers_garch
        
    Returns:
        Dictionary with validation results for each ticker
    """
    validation_results = {}
    
    for ticker, results in garch_results.items():
        validation = {
            'ticker': ticker,
            'model_converged': results['model'].convergence_flag if hasattr(results['model'], 'convergence_flag') else True,
            'persistence_stable': results['persistence'] < 1.0,  
            'alpha_significant': results['alpha'] > 0.01, 
            'beta_significant': results['beta'] > 0.01,   
            'adequate_sample': results['n_observations'] > 100,
            'warnings': []
        }
        
        if results['persistence'] >= 1.0:
            validation['warnings'].append("Non-stationary volatility (persistence ≥ 1)")
        
        if results['alpha'] < 0.01:
            validation['warnings'].append("Weak ARCH effect (α < 0.01)")
            
        if results['beta'] < 0.01:
            validation['warnings'].append("Weak GARCH effect (β < 0.01)")
        
        if results['n_observations'] < 100:
            validation['warnings'].append("Small sample size may affect reliability")
        
        validation_results[ticker] = validation
        
        status = "VALID" if not validation['warnings'] else "WARNING"
        logger.info(f"{ticker.upper()} validation: {status}")
        for warning in validation['warnings']:
            logger.warning(f"{ticker.upper()}: {warning}")
    
    return validation_results