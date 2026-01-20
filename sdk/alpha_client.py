import pandas as pd
from feast import FeatureStore
from datetime import datetime
import os

class AlphaWarehouse:
    def __init__(self, repo_path="feature_repo"):
        self.store = FeatureStore(repo_path=repo_path)

    def get_historical_features(self, tickers, start_date, end_date):
        print(f"Fetching features for {tickers} from {start_date} to {end_date}...")

        timestamps = pd.date_range(start=start_date, end=end_date, freq="h")
        
        entity_df = pd.DataFrame()
        for t in tickers:
            temp_df = pd.DataFrame({"event_timestamp": timestamps})
            temp_df["ticker"] = t
            entity_df = pd.concat([entity_df, temp_df])

        training_df = self.store.get_historical_features(
            entity_df=entity_df,
            features=[
                "technical_indicators:rsi_14",
                "technical_indicators:macd_line",
                "technical_indicators:volatility_24h"
            ]
        ).to_df()
        
        return training_df.sort_values(["ticker", "event_timestamp"])

    def get_online_features(self, ticker):
        features = self.store.get_online_features(
            features=[
                "technical_indicators:rsi_14",
                "technical_indicators:macd_line"
            ],
            entity_rows=[{"ticker": ticker}]
        ).to_dict()
        
        return features

if __name__ == "__main__":
    warehouse = AlphaWarehouse()

    df = warehouse.get_historical_features(
        tickers=["RELIANCE"], 
        start_date=datetime.now() - pd.Timedelta(days=5),
        end_date=datetime.now()
    )
    print("\n--- Backtest Data (PIT Correct) ---")
    print(df.head())

    live_data = warehouse.get_online_features("RELIANCE")
    print("\n--- Live Data (Latest from Store) ---")
    print(live_data)