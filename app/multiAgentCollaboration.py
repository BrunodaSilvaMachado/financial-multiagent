
import os
from dotenv import load_dotenv 


from app.FinancialAdvisorSystem import FinancialAdvisorSystem
from app.agents.AnalystAgent import AnalystAgent
from app.agents.CriticAgent import CriticAgent
from app.agents.LlamaAgent import LlamaAgent
from app.agents.MarketAgent import MarketAgent, MarketAgentBr

load_dotenv() 
__API_KEY__ = os.getenv('ALPHA_API_KEY') or ''

llama = LlamaAgent("gemma3:1b")
analyst_agent = AnalystAgent(llama)
critic_agent = CriticAgent(llama)

def _select_market_agent(exchange:str):
    if exchange == "br":
        return MarketAgentBr()
    elif exchange == "us":
        return MarketAgent(__API_KEY__)
    else:
        raise ValueError(f"Exchange '{exchange}' not supported. Use 'br' or 'us'.")

def run_multi_agent(ticker, horizon: str = "1mo", risk: str = "medium", exchange: str = "br") -> dict:
    """
    Executa o sistema multiagente para um ou vários tickers.
    
    Args:
        ticker (str | list[str]): Código(s) da ação. Ex: "PETR4" ou ["PETR4", "VALE3"].
        horizon (str): Horizonte de investimento (ex: "1mo").
        risk (str): Perfil de risco ("low", "medium", "high").
        exchange (str): Mercado alvo ("br" ou "usa").
    
    Returns:
        dict: Resultados das análises.
    """
    
    market_agent = _select_market_agent(exchange)
    advisor = FinancialAdvisorSystem(market_agent, analyst_agent, critic_agent)
    
    #suport a lista de tickers
    result = {}
    if isinstance(ticker, str):
        result[ticker] = advisor.run(ticker, horizon=horizon, risk=risk)
        return result
    elif isinstance(ticker, (list,tuple)):
        for t in ticker:
            try:
                result[t] = advisor.run(t, horizon=horizon, risk=risk)
            except Exception as e:
                result[t] = {"error": str(e)}
        return result
    else:
        raise ValueError("Ticker deve ser string ou lista de strings.")