CREATE SCHEMA IF NOT EXISTS marketpulse;

DROP TABLE IF EXISTS marketpulse.stg_stocks;

CREATE TABLE marketpulse.stg_stocks (
    ticker VARCHAR(10),
    date DATE,
    open DECIMAL(12,4),      
    high DECIMAL(12,4),       
    low DECIMAL(12,4),       
    close DECIMAL(12,4),     
    volume BIGINT,
    
    CONSTRAINT chk_positive_prices CHECK (
        open > 0 AND high > 0 AND low > 0 AND close > 0
    ),
    CONSTRAINT chk_high_low CHECK (high >= low),
    CONSTRAINT chk_volume_positive CHECK (volume >= 0)
);
