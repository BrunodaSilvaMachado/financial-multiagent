class FinancialAdvisorSystem:
    """
    FinancialAdvisorSystem orquestra as interações entre os agentes de mercado, analista e crítico para fornecer recomendações financeiras.
    Atributos:
        market_agent: Agente responsável por obter dados de mercado para um determinado ticker.
        analyst_agent: Agente responsável por analisar as características do mercado com base no horizonte de investimento e perfil de risco.
        critic_agent: Agente responsável por revisar e criticar a análise realizada.
    Métodos:
        __init__(market_agent, analyst_agent, critic_agent):
            Inicializa o FinancialAdvisorSystem com os agentes especificados.
        run(ticker: str, horizon="7d", risk="medium"):
            Executa o fluxo de trabalho de consultoria financeira:
                1. Obtém dados de mercado para o ticker informado.
                2. Realiza análise utilizando as características do mercado, horizonte de investimento e perfil de risco.
                3. Revisa a análise utilizando o agente crítico.
            Retorna um dicionário contendo o ticker, características do mercado, análise e revisão.
    """
    
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
