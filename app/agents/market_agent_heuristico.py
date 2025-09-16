import json
import os
import pandas as pd
import numpy as np
from typing import Dict, Any
from ..multiAgentCollaboration import _select_market_agent 

__cache_data_path__ = "data_cache/"

def load_sample_prices(ticker) -> pd.DataFrame:
    # POC: lê CSV de exemplo e filtra por ticker; ou substitua por API real
    cache_data_path = __cache_data_path__
    cache_file = f"{cache_data_path}sample_prices.csv"
    df = pd.read_csv(cache_file, parse_dates=["date"])
    if isinstance(ticker, str):
        return df[df["ticker"] == ticker].sort_values("date")
    elif isinstance(ticker, (list, tuple)):
        result = {}
        for t in ticker:
            result[t] = df[df["ticker"] == t].sort_values("date")
        return pd.DataFrame(result) 
    return pd.DataFrame()

def get_cache_prices(ticker, exchange):
    cache_data_path = __cache_data_path__
    df = pd.DataFrame()
    
    def __internal__load_data_cache__(cache_file):
        df = pd.DataFrame()
        if exchange == "br":
            cache_file += ".json"
            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    data = json.load(f)
                prices = data["results"][0]["historicalDataPrice"]
                df = pd.DataFrame(prices)
                df["date"] = pd.to_datetime(df["date"], unit="s")
                df = df.sort_values("date")
        elif exchange == "us":
            cache_file += ".csv"
            if os.path.exists(cache_file):
                df = pd.read_csv(cache_file, parse_dates=["date"])
                df["close"] = df["4. close"]
        return df
    
    if isinstance(ticker, str):
        cache_file = f"{cache_data_path}{ticker}"
        df = __internal__load_data_cache__(cache_file)
    elif isinstance(ticker, (list, tuple)):
        result = {}
        for t in ticker:
            cache_file = f"{cache_data_path}{ticker}"
            result[t] = __internal__load_data_cache__(cache_file)
        df = pd.DataFrame(result) 
    
    return df

def get_prices(ticker, exchange)-> pd.DataFrame:
    try:
        df = get_cache_prices(ticker, exchange)
    except Exception as e:
        print(f"[WARN] Falha ao carregar cache {ticker}: {e}")
        df = load_sample_prices(ticker)
    return df

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

def run_market_agent(ticker, exchange="br") -> Dict[str, Any]:
    try:
        market_agent = _select_market_agent(exchange)
        result = market_agent.run(ticker)
        result["history_len"] = len(result.get("data", []))
        return result
    except Exception as e:
        print(f"[WARN] MarketAgent failed: {e}. Falling back to heuristic.")
    
        df = get_prices(ticker, exchange)
        if df.empty:
            raise ValueError(f"No data for {ticker}")
        features = compute_features(df)
        return {"ticker": ticker, "features": features, "history_len": len(df)}
