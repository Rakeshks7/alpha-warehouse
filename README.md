# The Alpha Warehouse 

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Feast](https://img.shields.io/badge/Feast-0.34.0-orange)](https://feast.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()

**A production-grade Quantitative Feature Store designed to eliminate Look-Ahead Bias.**

This project implements a "Two-Speed" architecture common in high-frequency trading firms: an offline batch layer for historical backtesting and a low-latency online layer for live inference, both served from a single source of truth.

---

##  The Problem vs. The Solution

| The "Hello World" Approach | The Alpha Warehouse (This Project) |
| :--- | :--- |
| Calculates indicators inside the strategy loop. | Pre-calculates 5,000+ features nightly. |
| **High Risk:** Easy to accidentally peek at future data. | **Zero Risk:** Feast guarantees Point-in-Time (PIT) correctness. |
| Code duplication between Backtest and Live. | **Unified SDK:** Same API for history and live execution. |

##  Architecture

1.  **ETL Layer (`/etl`)**: Python scripts (Airflow-ready) that ingest raw OHLCV market data and compute technical factors (RSI, MACD, Volatility).
2.  **Feature Store (`/feature_repo`)**: Managed by **Feast**. It versions data timestamps and manages the Offline (Parquet) and Online (Redis/SQLite) stores.
3.  **Alpha SDK (`/sdk`)**: A researcher-friendly API that retrieves "Time-Travel" accurate data for backtesting.
4.  **Strategy Engine (`/strategy`)**: A vectorized backtesting engine that consumes data from the warehouse to simulate trading performance.

##  Tech Stack

* **Core:** Python 3.9+
* **Feature Store:** Feast (Open Source)
* **Data Processing:** Pandas, NumPy, TA-Lib (Technical Analysis Library)
* **Storage:** Parquet (Offline), SQLite/Redis (Online)

## Disclaimer

This software is for educational and research purposes only. It does not constitute financial advice. Algorithmic trading involves significant risk of loss. The authors are not responsible for any financial losses incurred from using this codebase.