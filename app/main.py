from fastapi import FastAPI, HTTPException
from app.schemas import RunRequest
from app.agents.market_agent_heuristico import run_market_agent
from app.agents.analyst_agent_heuristico import run_analyst_agent
from app.multiAgentCollaboration import run_multi_agent
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Financial Multiagent POC")

@app.post("/run")
def run_pipeline(req: RunRequest):
    """"
    A ideia aqui era comparar o sistema heuristico com o sistema multiagente e demosntar que o LLM é mais robusto.
    Executa o pipeline heurístico para um único ticker.
    """
    try:
        market_result = run_market_agent(req.ticker, req.exchange)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    features = market_result["features"]
    analyst = run_analyst_agent(features, horizon=req.horizon, risk=req.risk)
    return {
        "ticker": req.ticker,
        "features": features,
        "analysis": analyst,
        "meta": {"history_len": market_result["history_len"]}
    }

@app.get("/")
def health():
    return {"status":"ok"}

@app.post("/run_macro")
def run_macro_agent(req: RunRequest):
    """"
    Executa o sistema multiagente para um ou vários tickers.
    Faz o uso do mesmo esquema de request do sistema heurístico, mas o campo ticker pode ser uma lista.
    Faz uso de LLM para análise e crítica.
    """
    logger.info(f"Executando multiagente para {req.ticker} | exchange={req.exchange}")
    result = run_multi_agent(req.ticker, horizon=req.horizon, risk=req.risk, exchange=req.exchange)
    return result