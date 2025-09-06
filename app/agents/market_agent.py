import pandas as pd
import numpy as np
from typing import Dict, Any

def load_sample_prices(ticker: str) -> pd.DataFrame:
    # POC: lê CSV de exemplo e filtra por ticker; ou substitua por API real
    df = pd.read_csv("app/data/sample_prices.csv", parse_dates=["date"])
    return df[df["ticker"] == ticker].sort_values("date")

def compute_features(df: pd.DataFrame) -> Dict[str, Any]:
    # calcula features simples: retorno, vol, sma
    df = df.copy()
    df["ret"] = df["close"].pct_change()
    last = df.iloc[-1]
    returns_7 = df["ret"].tail(7).mean()
    vol_7 = df["ret"].tail(7).std()
    sma_5 = df["close"].tail(5).mean()
    sma_20 = df["close"].tail(20).mean() if len(df) >= 20 else df["close"].mean()
    features = {
        "last_price": float(last["close"]),
        "returns_7": float(returns_7 or 0.0),
        "vol_7": float(vol_7 or 0.0),
        "sma_5": float(sma_5),
        "sma_20": float(sma_20),
    }
    return features

def run_market_agent(ticker: str) -> Dict[str, Any]:
    df = load_sample_prices(ticker)
    if df.empty:
        raise ValueError(f"No data for {ticker}")
    features = compute_features(df)
    return {"ticker": ticker, "features": features, "history_len": len(df)}
