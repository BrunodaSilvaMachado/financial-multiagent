from app.agents.LlamaAgent import LlamaAgent


class AnalystAgent:
    
    """
    Classe responsável por gerar recomendações de investimento com base em dados de mercado.
    Utiliza o agente Llama para analisar as características do mercado, horizonte de investimento e perfil de risco.
    Atributos:
        llama (LlamaAgent): Instância do agente Llama para interagir com o modelo de linguagem.
    Métodos:
        __init__(llama_agent: LlamaAgent):
            Inicializa o AnalystAgent com uma instância do agente Llama.
        run(features: dict, horizon="7d", risk="medium") -> dict:
            Recebe características do mercado, horizonte de investimento e perfil de risco.
            Constrói um prompt para análise e obtém a resposta do modelo.
            Retorna um dicionário contendo a análise da recomendação.
    """
    def __init__(self, llama_agent: LlamaAgent):
        self.llama = llama_agent

    def run(self, features: dict, horizon="7d", risk="medium"):
        prompt = f"""
        Você é um analista financeiro.
        Use os seguintes dados:
        Último preço: {features['last_price']:.2f}
        Retorno médio 7 dias: {features['returns_7']:.4f}
        Volatilidade 7 dias: {features['vol_7']:.4f}
        SMA-5: {features['sma_5']:.2f}
        SMA-20: {features['sma_20']:.2f}

        Contexto:
        - Horizonte de investimento: {horizon}
        - Perfil de risco: {risk}

        Tarefa:
        Diga se a recomendação é BUY, HOLD ou SELL.
        Explique em até 3 frases o motivo, incluindo os indicadores usados.
        """
        response = self.llama.ask(prompt)
        return {"analysis": response}
