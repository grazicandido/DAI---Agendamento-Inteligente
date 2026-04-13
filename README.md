# DAI---Agendamento-Inteligente
Propomos um Agente de IA omnichannel que atua em tempo real via WhatsApp, App, Site e Telefone para eliminar as fricções da jornada de agendamento, desde a intenção até o comparecimento. A solução foca em ser proativa e resolutiva, garantindo que o paciente não desista do processo.

Foi desenvolvido o MVP da DAI em que demonstra a aplicação prática da Inteligência Artificial, integrando backend, processamento de linguagem natural e experiência conversacional. Foi criado também um front-end simples para exemplificar a conversa com a IA. O sistema funciona por meio de um fluxo conversacional. O usuário envia uma mensagem, que é processada pela API e a Inteligência Artificial retorna outra mensagem. 

O sistema foi desenvolvido utilizando as seguintes tecnologias:

•	Python: linguagem principal do projeto

•	FastAPI: framework utilizado para construção da API backend

•	Streamlit: utilizado para criação da interface simples de chat

•	Google Gemini (IA Generativa): responsável por interpretar as mensagens do usuário

•	Uvicorn: servidor ASGI para execução da aplicação

## Como rodar
py -m uvicorn main:app --reload

py -m streamlit run app.py


