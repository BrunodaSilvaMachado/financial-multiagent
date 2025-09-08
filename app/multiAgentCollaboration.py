
import os
import json
import requests
import numpy as np
from dotenv import load_dotenv 
from langchain_community.chat_models import ChatOllama


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

def run_multi_agent(ticker: str, horizon: str = "1mo", risk: str = "medium", exchange: str = "br") -> dict:
    if exchange == "br":
        market_agent = MarketAgentBr()
    else:
        market_agent = MarketAgent(__API_KEY__)
    advisor = FinancialAdvisorSystem(market_agent, analyst_agent, critic_agent)
    result = advisor.run(ticker, horizon=horizon, risk=risk)
    return result