from fastapi import FastAPI, HTTPException
from app.schemas import RunRequest
from app.agents.market_agent_heuristico import run_market_agent
from app.agents.analyst_agent_heuristico import run_analyst_agent

app = FastAPI(title="Financial Multiagent POC")

@app.post("/run")
def run_pipeline(req: RunRequest):
    try:
        market_result = run_market_agent(req.ticker)
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
