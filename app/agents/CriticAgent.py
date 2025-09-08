class CriticAgent:
    def __init__(self, llama_agent: LlamaAgent):
        self.llama = llama_agent

    def run(self, analysis: dict):
        prompt = f"""
        Você é um revisor de investimentos.
        Revise a seguinte recomendação de investimento:
        {analysis['analysis']}

        Tarefa:
        - Diga se a recomendação é coerente com os dados?
        - Diga se existe algum risco ou inconsistência?

        Responda de forma direta, curta, em bullet points.
        """
        review = self.llama.ask(prompt)
        return {"review": review}
