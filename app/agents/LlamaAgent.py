import requests


class LlamaAgent:
    def __init__(self, model="gemma3:1b", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def ask(self, prompt: str) -> str:
        resp = requests.post(self.url, json={"model": self.model, "prompt": prompt, "stream": False})
        return resp.json()["response"]
