# MarketPulse: Daily Volatility Analytics & Forecasting Dashboard

## Project Overview
MarketPulse is an automated analytics pipeline that provides portfolio managers, traders, and risk teams with unified volatility insights and predictive forecasting. The system processes one year of daily market data for major tech stocks, implementing advanced GARCH volatility modeling and delivering actionable insights through an interactive Power BI dashboard.

## Business Problem
- **Data Fragmentation:** Price history scattered across multiple sources requiring manual consolidation
- **Manual Workflows:** Error-prone, repetitive data processing for each analysis
- **Lack of Predictive Insights:** No forward-looking volatility forecasts for risk management
- **Limited Risk Assessment:** Backward-looking analysis without statistical modeling capabilities

## Technical Architecture

### Data Pipeline
```
Yahoo Finance API → Raw CSV → PostgreSQL Staging → Feature Engineering → GARCH Modeling → Power BI Dashboard
```

### Project Structure
```
MARKET_PULSE_DAILY_VOLATILITY_DASHBOARD/
├── config/
│   └── .env                          # Environment configuration
├── data/
│   ├── raw/                          # Yahoo Finance CSV downloads
│   ├── staged/                       # Processed datasets
│   │   └── forecasts/                # GARCH model outputs
├── docs/                             # Business documentation
├── report/                           # Power BI dashboard (.pbix)
├── sql/                              # Database schema
├── src/
│   ├── main/
│   │   ├── extract/                  # Data extraction modules
│   │   ├── transform/                # Data cleaning & feature engineering
│   │   ├── load/                     # Database integration
│   │   └── ml/                       # GARCH volatility modeling
│   └── utils/                        # Configuration, logging, database utilities
├── summary/                          # Executive presentation
└── tests/                            # Unit tests
```

## Key Features

### 1. Automated Data Pipeline
- **Yahoo Finance Integration:** Fetches 1 year of OHLCV data for AAPL, GOOGL, MSFT, TSLA
- **PostgreSQL Staging:** Reliable data persistence with validation constraints
- **Quality Assurance:** Comprehensive error handling and data validation

### 2. Financial Feature Engineering
- **Log Returns:** Daily returns calculated as ln(P_t/P_t-1) for statistical modeling
- **Rolling Volatility:** 14-day annualized volatility using √252 trading days factor
- **Risk Metrics:** Maximum daily loss/gain calculations and cumulative returns

### 3. Advanced Statistical Modeling
- **GARCH(1,1) Implementation:** Volatility forecasting with arch library
- **Model Validation:** AIC-based comparison and persistence analysis
- **14-Day Forecasts:** Forward-looking volatility predictions for tactical decisions

### 4. Interactive Dashboard
- **Executive Summary:** KPIs, price trends, and volatility comparisons
- **Risk Analytics:** Risk-return scatter plots with quadrant analysis
- **Volatility Forecasting:** Historical vs predicted volatility visualization

## Technical Requirements

### Python Environment
```bash
conda create -n marketpulse python=3.12
conda activate marketpulse
pip install -r requirements.txt
```

### Required Packages
- pandas, numpy: Data manipulation and analysis
- yfinance: Yahoo Finance API integration
- arch: GARCH volatility modeling
- sqlalchemy: Database connectivity
- matplotlib, seaborn: Data visualization

### Database Setup
```sql
-- Run sql/schema.sql to create PostgreSQL tables
CREATE SCHEMA marketpulse;
CREATE TABLE marketpulse.stg_stocks (...);
```

### Environment Configuration
Create `config/.env` with:
```
POSTGRES_HOST=localhost
POSTGRES_DB=marketpulse
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
TICKERS=AAPL,GOOGL,MSFT,TSLA
RAW_DATA_PATH=data/raw
STAGED_DATA_PATH=data/staged
FORECAST_HORIZON=14
```

## Usage

### Run Complete Pipeline
```bash
python src/main/main.py
```

### Individual Components
```bash
# Data extraction only
python src/main/extract/fetch_data.py

# Feature engineering only
python src/main/transform/calculate_returns_volatility.py

# GARCH modeling only
python src/main/ml/forecast_volatility.py
```

## Key Results

### GARCH Model Performance (AIC Rankings)
1. **MSFT:** 919.53 (best fit - predictable volatility patterns)
2. **AAPL:** 976.37 (good model performance)
3. **GOOGL:** 1045.94 (moderate volatility complexity)
4. **TSLA:** 1464.23 (high volatility, complex dynamics)

### Statistical Insights
- **High Persistence:** All models show 0.93-0.98 persistence indicating strong volatility clustering
- **TSLA Anomaly:** Pure GARCH effects (α≈0, β≈0.99) suggesting unique volatility behavior
- **Forecast Accuracy:** 14-day predictions with confidence intervals for risk planning

### Business Value
- **Risk Assessment:** Clear identification of high-risk/high-return positioning
- **Predictive Capabilities:** Forward-looking volatility for tactical decision-making
- **Portfolio Insights:** Cross-ticker volatility comparison and ranking

## 📁 File Outputs

### Primary Datasets
| File | Description | Size |
|------|-------------|------|
| `data/staged/processed_stocks.csv` | Complete dataset with all engineered features | 1,000 rows × 11 columns |
| `data/staged/forecasts/all_tickers_garch_forecasts.csv` | 14-day volatility predictions | 56 rows × 5 columns |
| `data/staged/forecasts/garch_model_comparison.csv` | Model performance metrics | 4 rows × 9 columns |

### Dashboard
- 📊 `report/Market_Pulse_BI_Report.pbix`: Interactive Power BI dashboard with 3 analytical pages

### Documentation  
- 📋 `docs/Market_Pulse_Business_Problem.pdf`: Detailed business requirements
- 📊 `docs/Market_Pulse_Data_Dictionary.xlsx`: Complete data schema and definitions

## ⚙️ Development Notes

### Data Quality
- **Expected Missing Values:** 4 daily returns, 56 volatility values (rolling window limitations)
- **Data Validation:** Automated quality checks for price ranges, extreme returns, and statistical properties
- **Error Handling:** Comprehensive logging and exception management throughout pipeline

### Production Considerations
- **Modular Design:** Separate extract, transform, and load components for maintainability
- **Configuration Management:** Environment-specific settings via `.env` files
- **Database Integration:** PostgreSQL staging with validation constraints and indexing

## 🔮 Future Enhancements

<details>
<summary>Click to expand roadmap</summary>

- **Real-time Data Feeds:** Integration with live market data APIs
- **Additional Models:** EGARCH, GJR-GARCH for asymmetric volatility effects  
- **Portfolio Optimization:** Multi-asset correlation analysis and risk budgeting
- **Anomaly Detection:** Statistical outlier identification for extreme market events
- **Web Interface:** Flask/FastAPI dashboard for real-time monitoring
- **Cloud Deployment:** AWS/Azure pipeline automation and scheduling

</details>

## 👨‍💻 Author

**Background:** Software Developer (1 year backend development experience) transitioning to quantitative finance. This project demonstrates domain knowledge acquisition in financial analytics, statistical modeling, and risk assessment for fintech career development.

**Technical Skills Demonstrated:**
- Production ETL pipeline development
- Advanced statistical modeling (GARCH)
- Financial domain expertise
- Database design and integration
- Business intelligence and visualization

## 📄 License

This project is for portfolio demonstration purposes.

---

<div align="center">

**⭐ If this project helped you, please give it a star! ⭐**

[📧 Contact](mailto:your-email@example.com) | [💼 LinkedIn](https://linkedin.com/in/yourprofile) | [🔗 Portfolio](https://yourportfolio.com)

</div>