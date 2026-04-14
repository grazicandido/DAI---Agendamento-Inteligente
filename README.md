# DAI: Agendamento Inteligente
DAI é uma agente de IA desenvolvida para otimizar o processo de agendamento de consultas, atuando como assistente conversacional em tempo real. A solução simula um atendimento inteligente, reduzindo etapas manuais e facilitando a comunicação entre usuário e sistema.

O projeto implementa um MVP que demonstra a aplicação prática de Inteligência Artificial combinada com backend em Python e processamento de linguagem natural. Também foi desenvolvido um front-end simples para simular a interação com o usuário.

O sistema funciona por meio de um fluxo conversacional: o usuário envia uma mensagem, que é processada pela API. Quando necessário, a IA interpreta a intenção e o sistema retorna uma resposta adequada ao contexto da conversa.

## Funcionalidades:

Interpretação de mensagens do usuário;

Fluxo de agendamento de consultas;

Identificação de intenção (agendar, cancelar, etc.);

Simulação de escolha de especialidade e horário;

Respostas contextuais com IA.

## O sistema foi desenvolvido utilizando as seguintes tecnologias:

•	Python: linguagem principal do projeto

•	FastAPI: framework utilizado para construção da API backend

•	Streamlit: utilizado para criação da interface simples de chat

•	Google Gemini (IA Generativa): responsável por interpretar as mensagens do usuário

•	Uvicorn: servidor ASGI para execução da aplicação

Este projeto foi desenvolvido como MVP para demonstrar a integração entre backend, IA generativa e fluxo conversacional estruturado.

## Como rodar
py -m uvicorn main:app --reload

py -m streamlit run app.py

Acrescente sua API key do gemini no arquivo main.py
