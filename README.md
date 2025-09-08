# Financial Multi-Agent Prototype (GenAI)

Este projeto foi desenvolvido como resposta ao **Desafio ICTi**:contentReference[oaicite:0]{index=0}, cujo objetivo é criar um protótipo funcional utilizando conceitos de **multiagentes de GenAI** aplicados ao **mundo financeiro**.

## 🎯 Objetivo

O protótipo simula um **assistente multiagente para decisões de investimento**:

- **Market Agent**: obtém preços históricos (via CSV ou API) e extrai *features* (retornos, volatilidade, médias móveis).
- **Analyst Agent**: recebe as *features* e gera uma recomendação (Buy / Hold / Sell) com justificativa textual.
- (Opcional) **Critic Agent**: valida as recomendações (checagem de consistência e risco).

Esse fluxo demonstra colaboração entre agentes e pode ser expandido para incluir **marketplace de agentes**, **tools** e **pipelines mais complexos**.

---

## 📂 Estrutura do Projeto

```txt
financial-multiagent/
├─ app/
│ ├─ main.py # Orquestrador (FastAPI)
│ ├─ schemas.py # Schemas de entrada/saída
│ ├─ agents/
│ │ ├─ market_agent.py # Agente de dados de mercado
│ │ └─ analyst_agent.py# Agente analista (LLM ou heurístico)
│ └─ data/
│ └─ sample_prices.csv # Dataset local de preços
├─ requirements.txt
└─ README.md
```

## Executar o projeto

Iniciar a fastApi

> uvicorn app.main:app --reload

Iniciar o frontend

> streamlit run app/frontend.py

Abra o navegador em: http://localhost:8501
