#  DAI – Agendamento Inteligente

DAI é uma agente de Inteligência Artificial desenvolvido para otimizar o processo de agendamento de consultas médicas, atuando como uma assistente virtual conversacional em tempo real.

A solução simula um atendimento inteligente, automatizando interações e facilitando a comunicação entre usuário e sistema de saúde.


## Objetivo

Resolver o problema de agendamentos demorados e manuais, utilizando IA para:

- Reduzir tempo de atendimento  
- Melhorar a experiência do usuário  
- Automatizar processos operacionais  

## Funcionalidades

- Interpretação de mensagens em linguagem natural  
- Identificação de intenção (consulta, exame, cancelamento, orientações)  
- Sugestão de horários baseada em dados reais  
- Confirmação de agendamento  
- Cancelamento de consultas  
- Respostas inteligentes com IA generativa  

## Arquitetura

O sistema foi estruturado com separação entre frontend e backend:

- **Backend (FastAPI)**: responsável pela lógica de negócio e integração com IA  
- **Frontend (Streamlit)**: interface conversacional para interação com o usuário  
- **IA (Google Gemini)**: interpretação das mensagens e geração de respostas  
- **Base de dados (Excel)**: utilizada para simular disponibilidade de agendas  

## Tecnologias utilizadas

- Python  
- FastAPI  
- Streamlit  
- Google Gemini (IA Generativa)  
- Pandas  
- Uvicorn  

## Diferenciais

- Aplicação real de IA em um cenário de saúde  
- Uso de dados estruturados (Excel) para simulação de agenda  
- Arquitetura desacoplada (API + Interface)  
- Fluxo completo ponta a ponta funcionando  

## Como rodar
### Backend
py -m uvicorn main:app --reload

Acrescente sua API key do gemini no arquivo main.py

Salve o arquivo do excel que está na pasta "dados"

### Frontend

py -m streamlit run app.py
salve o arquivo de imagem que está em "assets"
