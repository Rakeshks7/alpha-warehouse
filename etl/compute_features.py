import pandas as pd
import ta
import os
import sys

RAW_DATA_PATH = "data/raw/market_data_feed.parquet"
FEATURE_STORE_PATH = "data/features.parquet"

def load_raw_data():
    if not os.path.exists(RAW_DATA_PATH):
        print(f"[Error] Raw data not found at {RAW_DATA_PATH}.")
        print("Please run 'python etl/generator.py' first.")
        sys.exit(1)
        
    return pd.read_parquet(RAW_DATA_PATH)

def compute_technical_indicators(df):
    print("[Compute] Starting feature engineering...")

    processed_dfs = []
    
    for ticker, group in df.groupby("ticker"):
        group = group.sort_values("event_timestamp")

        group['rsi_14'] = ta.momentum.rsi(group['close'], window=14)

        macd_obj = ta.trend.MACD(group['close'])
        group['macd_line'] = macd_obj.macd()
        group['macd_signal'] = macd_obj.macd_signal()

        group['volatility_24h'] = group['close'].pct_change().rolling(window=24).std()
        
        processed_dfs.append(group)
        
    final_df = pd.concat(processed_dfs)

    initial_len = len(final_df)
    final_df = final_df.dropna()
    dropped_len = initial_len - len(final_df)
    
    print(f"[Compute] Dropped {dropped_len} rows due to indicator warm-up.")

    final_df.to_parquet(FEATURE_STORE_PATH)
    print(f"[Compute] Features saved to Feature Store: {FEATURE_STORE_PATH}")

if __name__ == "__main__":
    raw_df = load_raw_data()
    compute_technical_indicators(raw_df)