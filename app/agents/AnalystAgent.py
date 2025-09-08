class AnalystAgent:
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
