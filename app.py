import streamlit as st
import requests

st.title("DAI - Agendamento Inteligente")

if "chat" not in st.session_state:
    st.session_state.chat = []

msg = st.text_input("Digite sua mensagem")

if st.button("Enviar"):

    resposta = requests.post(
        "http://localhost:8000/chat",
        json={"texto": msg}
    )

    resposta_texto = resposta.json()["resposta"]

    st.session_state.chat.append(("Você", msg))
    st.session_state.chat.append(("DAI", resposta_texto))

for autor, texto in st.session_state.chat:
    st.write(f"**{autor}:** {texto}")