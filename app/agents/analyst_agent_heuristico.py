from typing import Dict, Any
import random

# POC: função que simula um LLM, baseada nas features retorna recomendação
def llm_stub_prompt(features: Dict[str, Any], horizon: str, risk: str) -> Dict[str, Any]:
    # Regras simples para demo:
    r = features["returns_7"]
    vol = features["vol_7"]
    sma5 = features["sma_5"]
    sma20 = features["sma_20"]

    # heurística simples
    score = 0
    if r > 0.003: score += 1
    if sma5 > sma20: score += 1
    if vol < 0.02: score += 1

    if score >= 2:
        action = "BUY"
    elif score == 1:
        action = "HOLD"
    else:
        action = "SELL"

    justification = (
        f"Score={score}. returns_7={r:.4f}, vol_7={vol:.4f}, sma5={sma5:.2f}, sma20={sma20:.2f}."
    )
    # Inclui pequenas variações para parecer mais 'natural'
    explanation = f"{justification} Recomendação para horizonte {horizon} com apetite {risk}: {action}."
    return {"action": action, "explanation": explanation, "confidence": round(0.6 + 0.1*score, 2)}

def run_analyst_agent(features: Dict[str, Any], horizon: str = "7d", risk: str = "medium") -> Dict[str, Any]:
    # Em produção aqui chamaria um LLM via API com um prompt estruturado
    return llm_stub_prompt(features, horizon, risk)
