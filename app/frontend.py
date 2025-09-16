import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/run_macro"

st.set_page_config(page_title="Financial Multi-Agent Advisor", page_icon="💹", layout="wide")

st.title("💹 Financial Multi-Agent Advisor")

st.markdown("Analise ações brasileiras (B3) e americanas (NASDAQ/NYSE) usando **agentes de IA**.")

# Inputs
ticker = st.text_input("Digite o ticker (ou vários separados por vírgula):", "PETR4, VALE3, ITUB4")
exchange = st.selectbox("Exchange", ["br", "us"])
horizon = st.selectbox("Horizonte de investimento", ["7d","1mo", "3mo", "6mo"])
risk = st.selectbox("Perfil de risco", ["low", "medium", "high"])

if st.button("Analisar"):
   # Exibe spinner enquanto processa
    with st.spinner("Processando dados..."):
        # Realiza a requisição
        tickers = [t.strip().upper() for t in ticker.split(",")]
        if len(tickers) == 1:
            tickers = tickers[0]  # envia como string se só um ticker

        payload = {
            "ticker": tickers,
            "horizon": horizon,
            "risk": risk,
            "exchange": exchange
        }

        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            st.subheader("📊 Resultados da análise")

            # Mostra cada ativo em um card
            for ticker, content in data.items():
                st.markdown(f"## 📈 {ticker}")
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.metric("💵 Último Preço", f"{content['features']['last_price']:.2f}")
                    st.metric("📉 Retorno (7d)", f"{content['features']['returns_7']:.4f}")
                    st.metric("📊 Volatilidade (7d)", f"{content['features']['vol_7']:.4f}")
                    st.metric("SMA-5", f"{content['features']['sma_5']:.2f}")
                    st.metric("SMA-20", f"{content['features']['sma_20']:.2f}")

                with col2:
                    st.markdown("### 🔎 Análise")
                    recommendation = content["analysis"]["analysis"]
                    if "BUY" in recommendation:
                        st.markdown(f"**Recomendação:** 🟩 :green[BUY]")  # Cartão verde
                    elif "SELL" in recommendation:
                        st.markdown(f"**Recomendação:** 🟥 :red[SELL]")  # Cartão vermelho
                    else:
                        st.markdown(f"**Recomendação:** 🟨 :yellow[HOLD]")  # Cartão amarelo
                    st.markdown(recommendation)

                    st.markdown("### 🧐 Revisão Crítica")
                    st.markdown(content["review"]["review"])

                st.markdown("---")

        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao conectar com a API: {e}")
