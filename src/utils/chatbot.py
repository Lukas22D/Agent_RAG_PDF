from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain.vectorstores import FAISS
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory

from dotenv import load_dotenv
import os

load_dotenv()

def create_vectorstore(chunks):
    """ Cria um vectorstore a partir dos chunks de texto, utilizando a Embedding API da Cohere e o FAISS """
    embeddings = CohereEmbeddings(cohere_api_key=os.getenv('COHERE_API_KEY'), model= 'embed-multilingual-v3.0')
    vectorstore = FAISS.from_texts(texts= chunks, embedding=embeddings)

    return vectorstore


# Dicionário para armazenar o histórico de mensagens do chat
store = {}

# Função para obter o histórico de uma sessão específica
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def create_conversation_chain(vectorstore):
    """ Cria uma cadeia de conversação a partir de um vectorstore e cria uma memória de conversação """
    llm = ChatCohere(cohere_api_key=os.getenv('COHERE_API_KEY'))
    # Define o prompt do sistema para contextualizar perguntas
    contextualize_q_system_prompt = ("Com base no chat history e a pergunta do usuário, faça analise do contexto e responda a pergunta do usuário.")
   # Cria um template de prompt de chat com a mensagem do sistema e um espaço reservado para o histórico do chat
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    # Cria um recuperador que leva em conta o histórico do chat
    history_aware_retriever = create_history_aware_retriever(
    llm, vectorstore.as_retriever(), contextualize_q_prompt
    )
    ### Responder a pergunta ###
    # Define o prompt do sistema para responder perguntas
    system_prompt = (
        "Do analysis and Respond to the user's question, "
        "referencing relevant Langchain features and documentation. Use the following context:\n\n"
        "{context}"
    )
    # Cria um template de prompt de chat com a mensagem do sistema e um espaço reservado para o histórico do chat
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    # Cria uma cadeia de documentos "stuff" para responder perguntas
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    # Cria uma cadeia de recuperação que combina o recuperador com consciência histórica e a cadeia de resposta de perguntas
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # Cria uma cadeia de recuperação conversacional com histórico de mensagens
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

  

    return conversational_rag_chain