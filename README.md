# 💹 Financial Multi-Agent Advisor

Protótipo funcional de um **sistema multiagente com GenAI** para análise de ações.
O projeto foi desenvolvido no contexto do **Desafio ICTi** e utiliza agentes colaborativos para recomendar estratégias de investimento com base em dados de mercado.

---

## 📌 Problema

Pequenos investidores e empresas têm dificuldade em priorizar ações/carteiras frente a notícias e sinais quantitativos.
Este protótipo implementa um **assistente multiagente** que integra:

* 📊 **Market Agent** → coleta dados de mercado (EUA e Brasil).
* 🤖 **Analyst Agent** → usa um LLM local (**Gemma3:1b via Ollama**) para gerar recomendações (BUY/HOLD/SELL).
* 🧐 **Critic Agent** → valida as recomendações e destaca riscos/inconsistências.

---

## ⚙️ Arquitetura

* **Backend:** FastAPI + Uvicorn
* **Frontend:** Streamlit
* **Agentes:** Market (Alpha Vantage / Brapi), Analyst (LLM), Critic (LLM)
* **LLM:** [Ollama](https://ollama.ai) rodando `gemma3:1b` localmente
* **Cache:** JSON/CSV local para confiabilidade mesmo offline

---

## 📂 Estrutura do repositório

``` bash
Multiagente Financeiro
|
|   LICENSE
|   README.md
|   requirements.txt
|
+---app
|   |   FinancialAdvisorSystem.py
|   |   frontend.py
|   |   main.py
|   |   multiAgentCollaboration.py
|   |   schemas.py
|   |
|   +---agents
|   |   |   AnalystAgent.py
|   |   |   analyst_agent_heuristico.py
|   |   |   CriticAgent.py
|   |   |   LlamaAgent.py
|   |   |   MarketAgent.py
|   |   |   market_agent_heuristico.py
|
+---data_cache
|       AAPL.csv
|       MSFT.csv
|       PETR4.json
|       VALE3.json
|       ITUB4.json
|       sample_prices.csv
|
+---notebook
    |   MultiAgentCollaborationHeuristico.ipynb
    |   MultiAgentCollaborationLLM.ipynb
```

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/multiagente-financeiro.git
cd multiagente-financeiro
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instale dependências

```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente

Crie um arquivo `.env` com:

```ini
ALPHA_API_KEY=YOUR_ALPHA_VANTAGE_KEY
```

> Para ações dos EUA.
> No Brasil (B3), a API **Brapi** não requer chave.

### 5. Instale e configure Ollama

Baixe [Ollama](https://ollama.ai) e rode:

```bash
ollama pull gemma3:1b
```

---

## ▶️ Como executar

### 1. Inicie a API FastAPI

```bash
uvicorn app.main:app --reload
```

API disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. Inicie o frontend Streamlit

Em outro terminal:

```bash
streamlit run app/frontend.py
```

Frontend disponível em: [http://localhost:8501](http://localhost:8501)

---

## 📡 Endpoints disponíveis

### 🔹 Healthcheck

```text
GET /
```

Resposta:

```json
{"status":"ok"}
```

---

### 🔹 Pipeline heurístico

```text
POST /run
```

Entrada:

```json
{
  "ticker": "PETR4",
  "horizon": "1mo",
  "risk": "medium",
  "exchange": "br"
}
```

Saída:

```json
{
  "ticker": "PETR4",
  "features": {...},
  "analysis": {...},
  "meta": {"history_len": 20}
}
```

---

### 🔹 Pipeline multiagente (LLM + Crítico)

```text
POST /run_macro
```

Entrada (um ou vários tickers):

```json
{
  "ticker": ["PETR4", "VALE3", "ITUB4"],
  "horizon": "1mo",
  "risk": "medium",
  "exchange": "br"
}
```

Saída:

```json
{
  "PETR4": {
    "ticker": "PETR4",
    "features": {...},
    "analysis": {...},
    "review": {...}
  },
  "VALE3": {...},
  "ITUB4": {...}
}
```

---

## 📊 Resultados obtidos

* ✅ Protótipo funcional implementado com FastAPI + Streamlit.
* ✅ Suporte a ações dos **EUA (Alpha Vantage)** e **Brasil (Brapi)**.
* ✅ Recomendações explicadas (LLM).
* ✅ Validação crítica de riscos (LLM).
* ✅ Interface amigável com cards em Streamlit.
