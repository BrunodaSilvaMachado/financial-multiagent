
import os
import json
import requests
import numpy as np
from dotenv import load_dotenv 
from langchain_community.chat_models import ChatOllama


from app import FinancialAdvisorSystem
from app.agents import LlamaAgent

load_dotenv() 
API_KEY = os.getenv('ALPHA_API_KEY')

llama = LlamaAgent("gemma3:1b")
#market_agent = MarketAgent(API_KEY)
market_agent = MarketAgentBr()
analyst_agent = AnalystAgent(llama)
critic_agent = CriticAgent(llama)

advisor = FinancialAdvisorSystem(market_agent, analyst_agent, critic_agent)

result = advisor.run("PETR4", horizon="1mo", risk="medium")
print(result)