# MarketPulse: Daily Volatility Analytics & Forecasting Dashboard

<div align="center">

![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-13+-blue.svg)
![PowerBI](https://img.shields.io/badge/powerbi-dashboard-yellow.svg)
![GARCH](https://img.shields.io/badge/modeling-GARCH(1,1)-green.svg)

</div>

## 📊 Project Overview

MarketPulse is an automated analytics pipeline that provides portfolio managers, traders, and risk teams with unified volatility insights and predictive forecasting. The system processes one year of daily market data for major tech stocks, implementing advanced GARCH volatility modeling and delivering actionable insights through an interactive Power BI dashboard.

## 🎯 Business Problem

- **Data Fragmentation:** Price history scattered across multiple sources requiring manual consolidation
- **Manual Workflows:** Error-prone, repetitive data processing for each analysis  
- **Lack of Predictive Insights:** No forward-looking volatility forecasts for risk management
- **Limited Risk Assessment:** Backward-looking analysis without statistical modeling capabilities

## 🏗️ Technical Architecture

### Data Pipeline
```mermaid
graph LR
    A[Yahoo Finance API] --> B[Raw CSV Files]
    B --> C[PostgreSQL Staging]
    C --> D[Feature Engineering]
    D --> E[GARCH Modeling]
    E --> F[Power BI Dashboard]
```

### Project Structure
```
MARKET_PULSE_DAILY_VOLATILITY_DASHBOARD/
├── 📁 config/
│   └── .env                          # Environment configuration
├── 📁 data/
│   ├── 📁 raw/                       # Yahoo Finance CSV downloads
│   └── 📁 staged/                    # Processed datasets & forecasts
├── 📁 docs/                          # Business documentation
│   ├── Market_Pulse_Business_Problem.pdf
│   ├── Market_Pulse_Methodology.pdf
│   └── Market_Pulse_Data_Dictionary.xlsx
├── 📁 report/                        # Power BI dashboard (.pbix)
├── 📁 sql/                           # Database schema
├── 📁 src/
│   ├── 📁 main/
│   │   ├── 📁 extract/               # Data extraction modules
│   │   ├── 📁 transform/             # Data cleaning & feature engineering
│   │   ├── 📁 load/                  # Database integration
│   │   └── 📁 ml/                    # GARCH volatility modeling
│   ├── 📁 utils/                     # Configuration, logging, database files
│   ├── 📁 logs/                      # Pipeline execution logs
│   ├── 📁 notebooks/                 # Jupyter analysis notebooks
│   └── 📁 tests/                     # Unit tests
├── 📁 summary/                       # Executive presentation
├── 📁 venv/                          # Virtual environment
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚡ Key Features

### 1. 🔄 Automated Data Pipeline
- **Yahoo Finance Integration:** Fetches 1 year of OHLCV data for AAPL, GOOGL, MSFT, TSLA
- **PostgreSQL Staging:** Reliable data persistence with validation constraints  
- **Quality Assurance:** Comprehensive error handling and data validation

### 2. 🧮 Financial Feature Engineering
- **Log Returns:** Daily returns calculated as `ln(P_t/P_t-1)` for statistical modeling
- **Rolling Volatility:** 14-day annualized volatility using `√252` trading days factor
- **Risk Metrics:** Maximum daily loss/gain calculations and cumulative returns

### 3. 📈 Advanced Statistical Modeling
- **GARCH(1,1) Implementation:** Volatility forecasting with `arch` library
- **Model Validation:** AIC-based comparison and persistence analysis
- **14-Day Forecasts:** Forward-looking volatility predictions for tactical decisions

### 4. 📊 Interactive Dashboard
- **Executive Summary:** KPIs, price trends, and volatility comparisons
- **Risk Analytics:** Risk-return scatter plots with quadrant analysis
- **Volatility Forecasting:** Historical vs predicted volatility visualization

## 🛠️ Technical Requirements

### Python Environment
```bash
conda create -n marketpulse python=3.12
conda activate marketpulse
pip install -r requirements.txt
```

### Required Packages
```txt
pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.0
arch>=6.0.0
sqlalchemy>=2.0.0
psycopg2>=2.9.0
matplotlib>=3.7.0
seaborn>=0.12.0
python-dotenv>=1.0.0
```

### Database Setup
```sql
-- Run sql/schema.sql to create PostgreSQL tables
CREATE SCHEMA IF NOT EXISTS marketpulse;
CREATE TABLE marketpulse.stg_stocks (
    ticker VARCHAR(10),
    date DATE,
    open DECIMAL(12,4),
    high DECIMAL(12,4),
    low DECIMAL(12,4),
    close DECIMAL(12,4),
    volume BIGINT
);
```

### Environment Configuration
Create `config/.env` file:
```env
POSTGRES_HOST=localhost
POSTGRES_DB=your_database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
TICKERS=AAPL,GOOGL,MSFT,TSLA
RAW_DATA_PATH=./data/raw/
STAGED_DATA_PATH=./data/staged/
FORECAST_HORIZON=14
```

## 🚀 Usage

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

## 📊 Key Results

### GARCH Model Performance (AIC Rankings)
| Rank | Ticker | AIC Score | Model Quality | Characteristics |
|------|--------|-----------|---------------|-----------------|
| 1    | MSFT   | 919.53    | ⭐⭐⭐⭐⭐        | Predictable volatility patterns |
| 2    | AAPL   | 976.37    | ⭐⭐⭐⭐         | Good model performance |
| 3    | GOOGL  | 1045.94   | ⭐⭐⭐          | Moderate volatility complexity |
| 4    | TSLA   | 1464.23   | ⭐⭐            | High volatility, complex dynamics |

### Statistical Insights
- **📈 High Persistence:** All models show 0.93-0.98 persistence indicating strong volatility clustering
- **⚡ TSLA Anomaly:** Pure GARCH effects (α≈0, β≈0.99) suggesting unique volatility behavior  
- **🎯 Forecast Accuracy:** 14-day predictions with confidence intervals for risk planning

### Business Value
- **🎯 Risk Assessment:** Clear identification of high-risk/high-return positioning
- **🔮 Predictive Capabilities:** Forward-looking volatility for tactical decision-making
- **📈 Portfolio Insights:** Cross-ticker volatility comparison and ranking

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
- **Database Integration:**  PostgreSQL staging capability implemented (current pipeline processes via CSV workflow for simplicity)

## 👨‍💻 Author

**Background:** Software Developer (1 year backend development experience) transitioning to data analytics. This project represents my first exploration into quantitative finance, demonstrating ability to acquire new domain knowledge in financial analytics, statistical modeling, and risk assessment.

**Technical Skills Demonstrated:**
- Production ETL pipeline development
- Advanced statistical modeling (GARCH)
- Financial domain expertise
- Database design and integration
- Business intelligence and visualization

## License

This project is for portfolio demonstration purposes.

---

<div align="center">

**⭐ If this project helped you, please give it a star! ⭐**

[📧 Contact](mailto:udit9503@gmail.com) | [💼 LinkedIn](https://www.linkedin.com/in/udit-singh-43862b187/)

</div>