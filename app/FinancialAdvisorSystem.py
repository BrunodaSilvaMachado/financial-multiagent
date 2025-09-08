class FinancialAdvisorSystem:
    def __init__(self, market_agent, analyst_agent, critic_agent):
        self.market_agent = market_agent
        self.analyst_agent = analyst_agent
        self.critic_agent = critic_agent

    def run(self, ticker: str, horizon="7d", risk="medium"):
        # 1. Dados de mercado
        market_result = self.market_agent.run(ticker)

        # 2. Análise
        analysis = self.analyst_agent.run(market_result["features"], horizon, risk)

        # 3. Crítica
        review = self.critic_agent.run(analysis)

        return {
            "ticker": ticker,
            "features": market_result["features"],
            "analysis": analysis,
            "review": review
        }
