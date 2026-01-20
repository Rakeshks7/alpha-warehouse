import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

RAW_DATA_DIR = "data/raw"
RAW_FILE_NAME = "market_data_feed.parquet"

def generate_market_feed(tickers, days_history=365):
    print(f"[Generator] Simulating data feed for: {tickers}")
    
    data_frames = []

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_history)
    dates = pd.date_range(start=start_date, end=end_date, freq="h")
    
    for ticker in tickers:
        np.random.seed(len(ticker) + int(start_date.timestamp()))
        
        returns = np.random.normal(0, 0.001, size=len(dates))
        price_path = 1000 * (1 + returns).cumprod()
        
        df = pd.DataFrame({
            "ticker": ticker,
            "event_timestamp": dates,
            "open": price_path, 
            "high": price_path * (1 + np.abs(np.random.normal(0, 0.005, len(dates)))),
            "low": price_path * (1 - np.abs(np.random.normal(0, 0.005, len(dates)))),
            "close": price_path * (1 + np.random.normal(0, 0.001, len(dates))),
            "volume": np.random.randint(1000, 500000, size=len(dates)).astype(float)
        })

        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].clip(lower=0.01)
        
        data_frames.append(df)
    
    full_df = pd.concat(data_frames).reset_index(drop=True)

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    output_path = os.path.join(RAW_DATA_DIR, RAW_FILE_NAME)
    full_df.to_parquet(output_path)
    
    print(f"[Generator] Raw data successfully landed at: {output_path}")
    print(f"[Generator] Total Rows: {len(full_df)}")

if __name__ == "__main__":
    generate_market_feed(tickers=["RELIANCE", "TCS", "INFY", "HDFCBANK"])