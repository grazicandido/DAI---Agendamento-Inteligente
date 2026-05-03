from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import pandas as pd

genai.configure(api_key="AIzaSyA9LwuvJ1rdGYR-QyqLsfFFTjcL9h9tSu0")
model = genai.GenerativeModel("models/gemini-flash-latest")

# APP FASTAPI
# =========================

app = FastAPI(title="DAI - Agendamento Inteligente")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CAMINHO DO EXCEL
# =========================

CAMINHO_EXCEL = "../dados/Agendamentos Exame e Consulta v1.xlsx"

# =========================
# MEMÓRIA TEMPORÁRIA
# =========================

agendamentos_confirmados = []

# =========================
# FUNÇÕES DE DADOS
# =========================

def carregar_base():
    return pd.read_excel(CAMINHO_EXCEL, sheet_name="Exportar Planilha")


def gerar_horarios_da_base(tipo_agenda=None):
    df = carregar_base()

    if tipo_agenda:
        df = df[df["TIPO_AGENDA"].astype(str).str.contains(tipo_agenda, case=False, na=False)]

    df = df.dropna(subset=["TIPO_AGENDA", "DS_UNIDADE_ATENDIMENTO"])

    amostra = df[[
        "TIPO_AGENDA",
        "DS_UNIDADE_ATENDIMENTO",
        "USUARIO",
        "CLUSTERR",
        "IDADE"
    ]].head(5)

    horas = ["08:30", "09:00", "10:30", "14:00", "15:30"]

    horarios = []

    for _, row in amostra.iterrows():
        horarios.append({
            "id": len(horarios) + 1,
            "tipo_agenda": str(row["TIPO_AGENDA"]),
            "unidade": str(row["DS_UNIDADE_ATENDIMENTO"]),
            "canal_origem": str(row["USUARIO"]),
            "cluster": str(row["CLUSTERR"]),
            "idade_referencia": int(row["IDADE"]) if pd.notna(row["IDADE"]) else None,
            "data_sugerida": "20/12/2025",
            "hora_sugerida": horas[len(horarios) % len(horas)],
            "status": "disponível"
        })

    return horarios

# =========================
# IA
# =========================

def responder_com_gemini(mensagem: str):
    prompt = f"""
    Você é a DAI, assistente de agendamento médico.

    Regras:
    - Seja curta, simpática e objetiva
    - Não pergunte por período do dia
    - Não reinicie a conversa
    - Se o usuário quiser agendar, diga que encontrou horários disponíveis

    Mensagem:
    {mensagem}
    """

    try:
        return model.generate_content(prompt).text
    except Exception as erro:
        return f"Erro na IA: {erro}"

# =========================
# INTENÇÃO
# =========================

def identificar_intencao(mensagem: str):
    texto = mensagem.lower()

    # 🔴 ENCERRAMENTO
    if any(p in texto for p in ["nenhum", "nenhuma", "não quero", "nao quero", "encerrar", "finalizar"]):
        return "encerrar"

    if "cancelar" in texto or "desmarcar" in texto:
        return "cancelamento"

    if "remarcar" in texto or "trocar horário" in texto:
        return "remarcacao" 

    if "orientação" in texto or "orientacoes" in texto or "orientações" in texto or "preparo" in texto:
        return "orientacao" 

    if "exame" in texto:
        return "exame"

    if "consulta" in texto or "marcar" in texto or "agendar" in texto:
        return "consulta"

    return "duvida"

# =========================
# ROTAS
# =========================

@app.get("/")
def home():
    return {"status": "DAI API funcionando"}


@app.post("/chat")
def chat(mensagem: str):
    intencao = identificar_intencao(mensagem)
    resposta_ia = responder_com_gemini(mensagem)

    if intencao == "encerrar":
        return {
            "acao": "encerrar",
            "mensagem": "Tudo bem 😊 Se precisar de algo no futuro, estou por aqui."
        }

    if intencao == "consulta":
        return {
            "acao": "mostrar_horarios",
            "mensagem": resposta_ia,
            "horarios": gerar_horarios_da_base("AMBULATORIAL")
        }

    if intencao == "orientacao":
        return {
            "acao": "orientacao",
            "mensagem": "Para exames, normalmente é importante confirmar se há necessidade de jejum, levar documento com foto, pedido médico e carteirinha do convênio. Também é recomendado chegar com antecedência e seguir a orientação específica do laboratório."
        }

    if intencao == "exame":
        return {
            "acao": "mostrar_horarios",
            "mensagem": resposta_ia,
            "horarios": gerar_horarios_da_base("IMAGEM")
        }

    if intencao == "cancelamento":
        return {
            "acao": "listar_agendamentos",
            "mensagem": "Qual agendamento deseja cancelar?",
            "agendamentos": agendamentos_confirmados
        }

    if intencao == "remarcacao":
        return {
            "acao": "remarcar",
            "mensagem": "Escolha um novo horário:",
            "horarios": gerar_horarios_da_base()
        }

    return {
        "acao": "responder",
        "mensagem": resposta_ia
    }

# =========================
# CONFIRMAR
# =========================

@app.post("/confirmar")
def confirmar_agendamento(id_horario: int):
    horarios = gerar_horarios_da_base()

    for h in horarios:
        if h["id"] == id_horario:
            agendamento = {
                "id_agendamento": len(agendamentos_confirmados) + 1,
                "status": "confirmado",
                "dados": h
            }

            agendamentos_confirmados.append(agendamento)

            return {
                "status": "confirmado",
                "mensagem": f"Agendamento confirmado para {h['hora_sugerida']} na {h['unidade']}",
                "agendamento": agendamento
            }

    return {"status": "erro"}

# =========================
# LISTAR
# =========================

@app.get("/meus-agendamentos")
def listar():
    return {"agendamentos": agendamentos_confirmados}

# =========================
# CANCELAR
# =========================

@app.post("/cancelar")
def cancelar(id_agendamento: int):
    for ag in agendamentos_confirmados:
        if ag["id_agendamento"] == id_agendamento:
            ag["status"] = "cancelado"
            return {"mensagem": "Cancelado com sucesso"}

    return {"erro": "não encontrado"}

# =========================
# REMARCAR
# =========================

@app.post("/remarcar")
def remarcar(id_agendamento: int, novo_id: int):
    horarios = gerar_horarios_da_base()

    for h in horarios:
        if h["id"] == novo_id:
            for ag in agendamentos_confirmados:
                if ag["id_agendamento"] == id_agendamento:
                    ag["dados"] = h
                    ag["status"] = "remarcado"

                    return {
                        "mensagem": f"Remarcado para {h['hora_sugerida']}",
                        "agendamento": ag
                    }

    return {"erro": "falha"}