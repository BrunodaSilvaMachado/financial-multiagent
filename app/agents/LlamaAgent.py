import requests


class LlamaAgent: 
    """
    A classe LlamaAgent representa um agente capaz de interagir com um modelo especificado via uma URL.

    O método __init__ inicializa os atributos 'model' e 'url' com valores padrão, caso não sejam fornecidos
    durante a criação do objeto.

    O método ask envia um prompt para o modelo usando uma requisição HTTP POST e retorna a resposta.

    Nota sobre o uso de requests:
    O pacote 'requests' é utilizado para realizar chamadas HTTP diretas à API do Ollama, proporcionando simplicidade
    e flexibilidade. Diferente de frameworks mais robustos, 'requests' permite uma integração rápida e leve, sem
    necessidade de configuração adicional, sendo ideal para interações pontuais ou scripts simples.
    """
    
    def __init__(self, model="gemma3:1b", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def ask(self, prompt: str) -> str:
        resp = requests.post(self.url, json={"model": self.model, "prompt": prompt, "stream": False})
        return resp.json()["response"]
