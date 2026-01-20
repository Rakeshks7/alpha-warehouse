import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sdk.alpha_client import AlphaWarehouse

class VectorizedBacktester:
    def __init__(self, ticker, start_date, end_date, initial_capital=100000.0):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.capital = initial_capital
        self.warehouse = AlphaWarehouse()
        self.data = None
        self.results = None

    def load_data(self):
        print(f"[Strategy] Fetching PIT data for {self.ticker}...")

        features_df = self.warehouse.get_historical_features(
            tickers=[self.ticker],
            start_date=self.start_date,
            end_date=self.end_date
        )

        raw_df = pd.read_parquet("data/raw/market_data_feed.parquet")
        price_df = raw_df[raw_df['ticker'] == self.ticker][['event_timestamp', 'close']]

        self.data = pd.merge_asof(
            features_df.sort_values('event_timestamp'),
            price_df.sort_values('event_timestamp'),
            on='event_timestamp',
            direction='backward'
        )
        self.data.set_index('event_timestamp', inplace=True)
        print(f"[Strategy] Data Loaded. Rows: {len(self.data)}")

    def generate_signals(self):
        if self.data is None:
            raise ValueError("Data not loaded. Run load_data() first.")

        df = self.data.copy()

        df['signal'] = 0

        df.loc[df['rsi_14'] < 30, 'signal'] = 1

        df.loc[df['rsi_14'] > 70, 'signal'] = -1

        df['position'] = df['signal'].replace(0, np.nan).ffill().fillna(0)

        df['position'] = df['position'].shift(1)
        
        self.data = df

    def run_backtest(self):
        print("[Strategy] Executing Vectorized Backtest...")
        df = self.data

        df['asset_returns'] = df['close'].pct_change()

        df['strategy_returns'] = df['position'] * df['asset_returns']

        df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()
        df['portfolio_value'] = self.capital * df['cumulative_returns']
        
        self.results = df
        return df

    def print_performance(self):
        if self.results is None:
            return

        total_return = self.results['cumulative_returns'].iloc[-1] - 1
        sharpe_ratio = self.results['strategy_returns'].mean() / self.results['strategy_returns'].std() * np.sqrt(252*7) # Annualized (assuming hourly data 7h/day)
        
        print("\n" + "="*40)
        print(f" PERFORMANCE REPORT: {self.ticker}")
        print("="*40)
        print(f"Initial Capital:   ${self.capital:,.2f}")
        print(f"Final Value:       ${self.results['portfolio_value'].iloc[-1]:,.2f}")
        print(f"Total Return:      {total_return*100:.2f}%")
        print(f"Sharpe Ratio:      {sharpe_ratio:.2f}")
        print("="*40 + "\n")

if __name__ == "__main__":
    TICKER = "RELIANCE"
    START = datetime.now() - timedelta(days=300)
    END = datetime.now()

    engine = VectorizedBacktester(TICKER, START, END)

    engine.load_data()       
    engine.generate_signals() 
    engine.run_backtest()     
    engine.print_performance()