from app.agents.LlamaAgent import LlamaAgent


class CriticAgent:
    """
    Classe responsável por revisar recomendações de investimento geradas por um agente Llama.
    Utiliza o agente Llama para analisar a recomendação, verificando sua coerência com os dados fornecidos
    e identificando possíveis riscos ou inconsistências. A resposta é direta e objetiva, apresentada em tópicos.
    Atributos:
        llama (LlamaAgent): Instância do agente Llama para interagir com o modelo de linguagem.
    Métodos:
        __init__(llama_agent: LlamaAgent):
            Inicializa o CriticAgent com uma instância do agente Llama.
        run(analysis: dict) -> dict:
            Recebe uma análise de investimento, constrói um prompt para revisão e obtém a resposta do modelo.
            Retorna um dicionário contendo a revisão da recomendação.
    """
    
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
