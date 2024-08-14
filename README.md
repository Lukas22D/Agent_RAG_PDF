# AGENTE RAG PDF

Este projeto permite que você faça perguntas diretamente para seus arquivos PDF. Ele utiliza o Streamlit para a interface de usuário e a Langchain para processar e interpretar os textos. A seguir, você encontrará detalhes sobre a estrutura do código e as funções principais utilizadas no projeto.

## Estrutura do Projeto
````
src/
├──utils/
|   ├── process.py
|   └── chatbot.py
└── app.py
 ````

### `app.py`

Este arquivo contém o código principal para executar o aplicativo Streamlit. Ele lida com a interface do usuário e a lógica para carregar os arquivos PDF, processá-los e fazer perguntas a eles.

#### Funções Principais

- **main()**: Configura a interface do Streamlit, recebe a entrada do usuário, gerencia o estado da sessão e invoca o chatbot para responder às perguntas baseadas nos textos dos PDFs carregados.
- **st.set_page_config**: Define o título e ícone da página.
- **st.text_input**: Recebe a pergunta do usuário.
- **st.file_uploader**: Permite o upload de múltiplos arquivos PDF.
- **st.session_state**: Armazena o estado da sessão, incluindo a ID da sessão e a conversa atual.
- **message()**: Exibe mensagens do usuário e do bot no chat.

### `process.py`

Este módulo contém funções para processamento de arquivos PDF e divisão do texto em "chunks".

#### Funções Principais

- **process_files(files)**: Processa os arquivos PDF e extrai o texto deles.
- **crate_text_chunks(text)**: Divide o texto em chunks de 1000 caracteres com sobreposição de 300 caracteres.

### `chatbot.py`

Este módulo lida com a criação do vetor de armazenamento (`vectorstore`) e a configuração da cadeia de conversação para o chatbot.

#### Funções Principais

- **create_vectorstore(chunks)**: Cria um vetor de armazenamento a partir dos chunks de texto utilizando as Embeddings da API da Cohere e FAISS.
- **get_session_history(session_id)**: Recupera o histórico de mensagens de uma sessão específica.
- **create_conversation_chain(vectorstore)**: Cria uma cadeia de conversação que utiliza um vetor de armazenamento e mantém um histórico de conversas.

### Requisitos

Para rodar este projeto, certifique-se de ter as seguintes bibliotecas instaladas:

```bash
pip install streamlit PyPDF2 langchain-cohere langchain-core langchain-community python-dotenv
```

### Executando o Projeto
- **Faça o upload dos seus arquivos PDF pela interface.**
- **Digite uma pergunta relacionada ao conteúdo dos PDFs.**
- **O bot responderá com base nas informações extraídas dos documentos.**
