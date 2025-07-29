CREATE SCHEMA IF NOT EXISTS marketpulse;

CREATE TABLE IF NOT EXISTS marketpulse.stg_stocks (
  ticker VARCHAR,
  date   DATE,
  open   INT,
  high   INT,
  low    INT,
  close  INT,
  volume BIGINT
);
