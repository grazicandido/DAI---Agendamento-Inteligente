import streamlit as st
import requests
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DAI - Agendamento Inteligente",
    page_icon="🩺",
    layout="centered"
)

# =========================
# CSS / VISUAL
# =========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #eef8ff 0%, #f7fbff 100%);
}

.main-card {
    background: linear-gradient(135deg, #3da9fc, #50c878);
    padding: 28px;
    border-radius: 26px;
    color: white;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.12);
    margin-bottom: 20px;
}

.service-card {
    background: white;
    padding: 18px;
    border-radius: 20px;
    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
    margin-bottom: 12px;
    min-height: 110px;
}

.appointment-card {
    background: white;
    padding: 18px;
    border-radius: 20px;
    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
    margin-bottom: 14px;
    border-left: 6px solid #3da9fc;
}

.chat-user {
    background: #d9ecff;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px auto;
    max-width: 85%;
    text-align: right;
    color: #073b4c;
}

.chat-bot {
    background: #e9f8ef;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px auto 8px 0;
    max-width: 85%;
    color: #073b4c;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #073b4c;
    margin-top: 24px;
    margin-bottom: 12px;
}

.small-text {
    color: #5c6b73;
    font-size: 14px;
}

.status-ok {
    color: #16a34a;
    font-weight: bold;
}

.status-cancelado {
    color: #dc2626;
    font-weight: bold;
}

.status-remarcado {
    color: #f59e0b;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "chat" not in st.session_state:
    st.session_state.chat = []

if "horarios" not in st.session_state:
    st.session_state.horarios = []

if "agendamento_confirmado" not in st.session_state:
    st.session_state.agendamento_confirmado = None

if "agendamentos" not in st.session_state:
    st.session_state.agendamentos = []

# =========================
# HEADER
# =========================

col_img, col_texto = st.columns([1, 5])

with col_img:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if Path("assets/dai_logo.png").exists():
        st.image("assets/dai_logo.png", width=220)

with col_texto:
    st.markdown("""
    <div class="main-card">
        <h1>Bem vindo(a)!</h1>
        <p>Sou a DAI, sua assistente inteligente de agendamento.</p>
        <p><b>Agende consultas, exames e retornos de forma rápida, simples e humanizada.</b></p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FUNÇÃO AUXILIAR
# =========================

def enviar_mensagem_padrao(texto_usuario):
    resposta = requests.post(
        f"{API_URL}/chat",
        params={"mensagem": texto_usuario}
    ).json()

    st.session_state.chat.append(("Você", texto_usuario))
    st.session_state.chat.append(("DAI", resposta.get("mensagem", "")))

    if resposta.get("horarios"):
        st.session_state.horarios = resposta.get("horarios", [])

    if resposta.get("agendamentos"):
        st.session_state.agendamentos = resposta.get("agendamentos", [])

# =========================
# CARDS DE SERVIÇOS
# =========================

st.markdown('<div class="section-title">O que você precisa hoje?</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="service-card">
        <h4>🩺 Consultas</h4>
        <p class="small-text">Encontre horários disponíveis para atendimento médico.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Agendar consulta", use_container_width=True):
        enviar_mensagem_padrao("quero agendar consulta")

with col2:
    st.markdown("""
    <div class="service-card">
        <h4>🧪 Exames</h4>
        <p class="small-text">Consulte unidades e opções disponíveis para exames.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Agendar exame", use_container_width=True):
        enviar_mensagem_padrao("quero agendar exame")

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="service-card">
        <h4>🔁 Retorno médico</h4>
        <p class="small-text">Agende um retorno com o médico de forma simples.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Agendar retorno", use_container_width=True):
        enviar_mensagem_padrao("quero agendar retorno médico")

with col4:
    st.markdown("""
    <div class="service-card">
        <h4>📓 Orientações</h4>
        <p class="small-text">Veja preparos, documentos e dicas importantes.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Ver orientações", use_container_width=True):
        st.session_state.chat.append(("Você", "quero orientações"))
        st.session_state.chat.append((
            "DAI",
            "Claro! Para consultas, leve documento com foto, carteirinha do convênio e exames anteriores, se tiver. "
            "Para exames, confira se existe preparo específico, como jejum, pedido médico ou autorização do convênio. "
            "Chegue com alguns minutos de antecedência para garantir um atendimento tranquilo."
        ))
        st.session_state.horarios = []

# =========================
# CHAT
# =========================

st.markdown('<div class="section-title">Converse com a DAI</div>', unsafe_allow_html=True)

mensagem = st.text_input(
    "Digite sua mensagem:",
    placeholder="Ex: quero agendar consulta de clínico geral"
)

col_enviar, col_limpar = st.columns([2, 1])

with col_enviar:
    enviar = st.button("Enviar mensagem", use_container_width=True)

with col_limpar:
    limpar = st.button("Nova conversa", use_container_width=True)

if limpar:
    st.session_state.chat = []
    st.session_state.horarios = []
    st.session_state.agendamento_confirmado = None
    st.session_state.agendamentos = []
    st.rerun()

if enviar and mensagem.strip():
    try:
        resposta = requests.post(
            f"{API_URL}/chat",
            params={"mensagem": mensagem}
        ).json()

        st.session_state.chat.append(("Você", mensagem))
        st.session_state.chat.append(("DAI", resposta.get("mensagem", "")))

        if resposta.get("acao") == "encerrar":
            st.session_state.horarios = []

        elif resposta.get("horarios"):
            st.session_state.horarios = resposta["horarios"]

        elif resposta.get("agendamentos"):
            st.session_state.agendamentos = resposta["agendamentos"]

    except Exception as erro:
        st.error(f"Erro ao conectar com o backend: {erro}")

# =========================
# HISTÓRICO DO CHAT
# =========================

for autor, texto in st.session_state.chat:
    if autor == "Você":
        st.markdown(f'<div class="chat-user"><b>Você:</b><br>{texto}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot"><b>DAI:</b><br>{texto}</div>', unsafe_allow_html=True)

# =========================
# HORÁRIOS SUGERIDOS
# =========================

if st.session_state.horarios:
    st.markdown('<div class="section-title">Horários sugeridos</div>', unsafe_allow_html=True)

    for h in st.session_state.horarios:
        st.markdown(f"""
        <div class="appointment-card">
            <h4>{h.get('tipo_agenda', 'Agenda disponível')}</h4>
            <p><b>Unidade:</b> {h.get('unidade', '-')}</p>
            <p><b>Data:</b> {h.get('data_sugerida', '-')} &nbsp; | &nbsp; <b>Hora:</b> {h.get('hora_sugerida', '-')}</p>
            <p><b>Status:</b> <span class="status-ok">{h.get('status', 'disponível')}</span></p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Confirmar horário {h['id']}", key=f"confirmar_{h['id']}", use_container_width=True):
            try:
                confirmacao = requests.post(
                    f"{API_URL}/confirmar",
                    params={"id_horario": h["id"]}
                ).json()

                st.session_state.agendamento_confirmado = confirmacao
                st.session_state.chat.append(("DAI", confirmacao.get("mensagem", "")))

                resposta_atualizada = requests.get(f"{API_URL}/meus-agendamentos").json()
                st.session_state.agendamentos = resposta_atualizada.get("agendamentos", [])

                st.success(confirmacao.get("mensagem", "Agendamento confirmado!"))

            except Exception as erro:
                st.error(f"Erro ao confirmar agendamento: {erro}")

# =========================
# AGENDAMENTO CONFIRMADO
# =========================

if st.session_state.agendamento_confirmado:
    st.markdown('<div class="section-title">Agendamento confirmado</div>', unsafe_allow_html=True)

    ag = st.session_state.agendamento_confirmado.get("agendamento", {})
    dados = ag.get("dados", {})

    st.markdown(f"""
    <div class="appointment-card">
        <h4>✅ Agendamento confirmado</h4>
        <p><b>ID do agendamento:</b> {ag.get("id_agendamento", "-")}</p>
        <p><b>Status:</b> <span class="status-ok">{ag.get("status", "-")}</span></p>
        <p><b>Tipo de agenda:</b> {dados.get("tipo_agenda", "-")}</p>
        <p><b>Unidade:</b> {dados.get("unidade", "-")}</p>
        <p><b>Data:</b> {dados.get("data_sugerida", "-")} &nbsp; | &nbsp; <b>Hora:</b> {dados.get("hora_sugerida", "-")}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# MEUS AGENDAMENTOS
# =========================

st.markdown('<div class="section-title">Meus agendamentos</div>', unsafe_allow_html=True)

if st.button("Atualizar meus agendamentos", use_container_width=True):
    try:
        resposta = requests.get(f"{API_URL}/meus-agendamentos").json()
        st.session_state.agendamentos = resposta.get("agendamentos", [])
    except Exception as erro:
        st.error(f"Erro ao buscar agendamentos: {erro}")

if st.session_state.agendamentos:
    for ag in st.session_state.agendamentos:
        dados = ag.get("dados", {})
        status = ag.get("status", "-")

        classe_status = "status-ok"
        if status == "cancelado":
            classe_status = "status-cancelado"
        elif status == "remarcado":
            classe_status = "status-remarcado"

        st.markdown(f"""
        <div class="appointment-card">
            <h4>Agendamento #{ag.get("id_agendamento")}</h4>
            <p><b>Status:</b> <span class="{classe_status}">{status}</span></p>
            <p><b>Tipo de agenda:</b> {dados.get("tipo_agenda", "-")}</p>
            <p><b>Unidade:</b> {dados.get("unidade", "-")}</p>
            <p><b>Data:</b> {dados.get("data_sugerida", "-")} &nbsp; | &nbsp; <b>Hora:</b> {dados.get("hora_sugerida", "-")}</p>
        </div>
        """, unsafe_allow_html=True)

        if status != "cancelado":
            if st.button(f"Cancelar agendamento {ag.get('id_agendamento')}", key=f"cancelar_{ag.get('id_agendamento')}", use_container_width=True):
                resposta = requests.post(
                    f"{API_URL}/cancelar",
                    params={"id_agendamento": ag.get("id_agendamento")}
                ).json()

                st.success(resposta.get("mensagem", "Cancelado com sucesso."))
                resposta_atualizada = requests.get(f"{API_URL}/meus-agendamentos").json()
                st.session_state.agendamentos = resposta_atualizada.get("agendamentos", [])
                st.rerun()
else:
    st.info("Nenhum agendamento confirmado ainda.")