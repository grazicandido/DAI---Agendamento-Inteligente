from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import json
import os

#API
client = genai.Client(api_key=("X"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Mensagem(BaseModel):
    texto: str

#Como está o agendamento

estado = {
    "etapa": None,
    "especialidade": None,
    "horario": None
}

#Interpretação da intenção

def interpretar_intencao(texto):
    t = texto.lower().strip()

    if any(p in t for p in ["consulta", "agendar", "marcar", "consultar", "médico", "exame"]):
        return {"intencao": "agendar_consulta", "especialidade": ""}

    if t in ["sim", "quero", "ok", "claro", "pode ser", "com certeza"]:
        return {"intencao": "agendar_consulta", "especialidade": ""}

    try:
        resposta = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""Analise o texto: "{texto}"
Responda apenas JSON:
- "intencao": "agendar_consulta" ou "outro"
- "especialidade": apenas se houver
Se for resposta positiva, trate como agendamento."""
        )

        limpo = resposta.text.replace("```json", "").replace("```", "").strip()
        return json.loads(limpo)
    except:
        return {"intencao": "outro", "especialidade": ""}

# Cancelamento do agendamento

def detectar_cancelamento(texto):
    t = texto.lower().strip()
    if t in ["nenhum", "nenhuma", "outro", "outros", "não", "nao", "cancelar", "desistir"]:
        return True
    try:
        resposta = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""Classifique o texto: "{texto}"
Responda apenas JSON:
- "acao": "cancelar" ou "continuar" """
        )
        limpo = resposta.text.replace("```json", "").replace("```", "").strip()
        dados = json.loads(limpo)
        return dados.get("acao") == "cancelar"
    except:
        return False


# Confirmação do horário

def parece_horario_valido(texto):
    t = texto.lower().strip()
    invalidos = ["nenhum", "nenhuma", "não sei", "nada"]
    if any(v in t for v in invalidos):
        return False
    if ":" in t or any(x in t for x in ["amanhã", "hoje", "dia", "segunda", "terça", "quarta", "quinta", "sexta"]):
        return True
    return False


# Endpoint

@app.post("/chat")
def chat(mensagem: Mensagem):
    global estado
    texto = mensagem.texto # Ajustado de 'message' para 'mensagem' para funcionar

    if estado["etapa"] == "aguardando_especialidade":
        estado["especialidade"] = texto
        estado["etapa"] = "aguardando_horario"

        return {
            "resposta": f"Entendido! Para {estado['especialidade']}, encontrei estes horários disponíveis na rede Mater Dei: \n\n📅 Amanhã às 10h\n📅 Hoje às 15h\n📅 Dia 23/04 às 12h\n\nAlgum destes funciona bem para você?",
            "intencao": "escolher_horario"
        }

    if estado["etapa"] == "aguardando_horario":
        if detectar_cancelamento(texto):
            estado["etapa"], estado["especialidade"], estado["horario"] = None, None, None
            return {
                "resposta": "Sem problemas. Interrompi o agendamento por aqui. Se mudar de ideia ou precisar de outra coisa, é só me chamar! 😊",
                "intencao": "cancelado"
            }

        if not parece_horario_valido(texto):
            return {
                "resposta": "Poxa, não consegui identificar um horário válido na sua mensagem. Para não agendarmos nada errado, vou encerrar este contato, mas você pode tentar novamente quando quiser!",
                "intencao": "reoferecer_horarios"
            }

        estado["horario"] = texto
        resposta_final = f"Confirmado com sucesso! ✅\nSua consulta de {estado['especialidade']} ficou para {estado['horario']}.\n\nEstamos ansiosos para cuidar de você!A Mater Dei agradece pela preferência! "

        estado["etapa"], estado["especialidade"], estado["horario"] = None, None, None
        return {
            "resposta": resposta_final,
            "intencao": "finalizado"
        }

    # Fluxo do agendamento
    dados = interpretar_intencao(texto)

    if dados.get("intencao") == "agendar_consulta":
        estado["etapa"] = "aguardando_especialidade"
        if dados.get("especialidade"):
            estado["especialidade"] = dados["especialidade"]
            estado["etapa"] = "aguardando_horario"
            return {
                "resposta": f"Com certeza! Verifiquei aqui e para {estado['especialidade']} temos estas opções:\n\n📅 Amanhã às 10h\n📅 Hoje às 15h\n📅 Dia 23/04 às 12h\n\nQual delas você prefere reservar?",
                "intencao": "escolher_horario"
            }
        return {
            "resposta": "Claro, fico feliz em ajudar com isso! Para qual especialidade médica você deseja realizar o agendamento?",
            "intencao": "pergunta"
        }

    #Default
    return {
        "resposta": "Olá! Eu sou o DAI, seu assistente de saúde inteligente. Como posso facilitar o seu dia hoje? Gostaria de marcar uma consulta?",
        "intencao": "ajuda"
    }