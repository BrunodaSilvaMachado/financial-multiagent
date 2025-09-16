from typing import Dict, Any
import random

# POC: função que simula um LLM, baseada nas features retorna recomendação
def llm_stub_prompt(features: Dict[str, Any], horizon: str, risk: str) -> Dict[str, Any]:
    # Regras simples para demo:
    r = features["returns_7"]
    vol = features["vol_7"]
    sma5 = features["sma_5"]
    sma20 = features["sma_20"]

    # heurística aprimorada considerando horizonte e risco
    score = 0
    # Ajusta thresholds conforme horizonte
    if horizon == "6mo":
        retorno_min = 0.01
        vol_max = 0.05
    elif horizon == "3mo":
        retorno_min = 0.007
        vol_max = 0.04
    elif horizon == "1mo":
        retorno_min = 0.005
        vol_max = 0.03
    else:  # padrão 7d
        retorno_min = 0.003
        vol_max = 0.02

    # Ajusta thresholds conforme risco
    if risk == "high":
        vol_max += 0.01
        retorno_min -= 0.001
    elif risk == "low":
        vol_max -= 0.005
        retorno_min += 0.001

    def interpret_return(r, retorno_min):
        if r > retorno_min:
            return 1, f"Retorno 7d de {r:.4f} está acima do mínimo ({retorno_min:.4f}), indicando força no desempenho."
        return 0, f"Retorno 7d de {r:.4f} está abaixo do mínimo ({retorno_min:.4f}), desempenho fraco."

    def interpret_sma(sma5, sma20):
        if sma5 > sma20:
            return 1, f"SMA-5 ({sma5:.2f}) maior que SMA-20 ({sma20:.2f}), tendência de alta no curto prazo."
        return 0, f"SMA-5 ({sma5:.2f}) menor ou igual a SMA-20 ({sma20:.2f}), tendência neutra ou de baixa."

    def interpret_vol(vol, vol_max, risk):
        if vol < vol_max:
            return 1, f"Volatilidade ({vol:.4f}) está abaixo do máximo ({vol_max:.4f}) para perfil {risk}, risco controlado."
        return 0, f"Volatilidade ({vol:.4f}) acima do máximo ({vol_max:.4f}) para perfil {risk}, risco elevado."

    interpretations = []
    s, interp = interpret_return(r, retorno_min)
    score += s
    interpretations.append(interp)

    s, interp = interpret_sma(sma5, sma20)
    score += s
    interpretations.append(interp)

    s, interp = interpret_vol(vol, vol_max, risk)
    score += s
    interpretations.append(interp)

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
    explanation = f"{justification} Recomendação para horizonte {horizon} com apetite {risk}: {action}.\nPrincipais métricas:\n- {interpretations[0]}\n- {interpretations[1]}\n- {interpretations[2]}"
    return {"action": action, "explanation": explanation, "confidence": round(0.6 + 0.1*score, 2)}

def run_analyst_agent(features: Dict[str, Any], horizon: str = "7d", risk: str = "medium") -> Dict[str, Any]:
    # Em produção aqui chamaria um LLM via API com um prompt estruturado
    return llm_stub_prompt(features, horizon, risk)
