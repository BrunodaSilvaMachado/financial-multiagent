import os
import pandas as pd
from typing import Dict, Any
from alpha_vantage.timeseries import TimeSeries
import requests

class MarketAgent:
    def __init__(self, api_key: str, cache_dir="data_cache", outputsize="compact"):
        self.ts = TimeSeries(key=api_key, output_format="pandas")
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.outputsize = outputsize

    def run(self, ticker: str):
        cache_file = f"{self.cache_dir}/{ticker}.csv"
        try:
            # Tenta buscar dados da API
            df, meta = self.ts.get_daily(symbol=ticker, outputsize=self.outputsize)
            df = df.sort_index()
            df.to_csv(cache_file)  # salva no cache
            print(f"[INFO] Dados baixados online para {ticker}.")
        except Exception as e:
            print(f"[WARN] Falha ao baixar {ticker}: {e}")
            if os.path.exists(cache_file):
                df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
                print(f"[INFO] Usando cache local: {cache_file}")
            else:
                raise RuntimeError(f"Sem dados disponíveis para {ticker}")

        # Calcula features
        df["ret"] = df["4. close"].pct_change()
        features = {
            "last_price": float(df["4. close"].iloc[-1]),
            "returns_7": float(df["ret"].tail(7).mean()),
            "vol_7": float(df["ret"].tail(7).std()),
            "sma_5": float(df["4. close"].tail(5).mean()),
            "sma_20": float(df["4. close"].tail(20).mean()),
        }
        return {"ticker": ticker, "features": features}

class Brapi:
    def __init__(self):
        self.base_url = "https://brapi.dev/api/quote"
        
    def get_dalay(self, ticker, drange="1mo", interval="1d"):
        build_url = f"{self.base_url}/{ticker}?range={drange}&interval={interval}"
        response = requests.get(build_url)
        return response.json()
    
class MarketAgentBr:
    def __init__(self, cache_dir="data_cache"):
        self.cache_dir = cache_dir
        self.ts = Brapi()
        os.makedirs(cache_dir, exist_ok=True)

    def run(self, ticker: str):
        cache_file = f"{self.cache_dir}/{ticker}.json"
        try:
            data = self.ts.get_dalay(ticker)

            if "results" not in data:
                raise ValueError(f"Nenhum dado encontrado para {ticker}")

            # salva cache
            with open(cache_file, "w") as f:
                json.dump(data, f)

            print(f"[INFO] Dados baixados online para {ticker}.")
        except Exception as e:
            print(f"[WARN] Falha ao baixar {ticker}: {e}")
            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    data = json.load(f)
                print(f"[INFO] Usando cache local: {cache_file}")
            else:
                raise RuntimeError(f"Sem dados disponíveis para {ticker}")

        # transforma em dataframe para calcular indicadores
        prices = data["results"][0]["historicalDataPrice"]
        df = pd.DataFrame(prices)
        df["date"] = pd.to_datetime(df["date"], unit="s")
        df = df.sort_values("date")
        df["ret"] = df["close"].pct_change()

        # features
        features = {
            "last_price": float(df["close"].iloc[-1]),
            "returns_7": float(df["ret"].tail(7).mean()),
            "vol_7": float(df["ret"].tail(7).std()),
            "sma_5": float(df["close"].tail(5).mean()),
            "sma_20": float(df["close"].tail(20).mean()),
        }
        return {"ticker": ticker, "features": features}
