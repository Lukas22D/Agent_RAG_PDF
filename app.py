import streamlit as st 
from utils import chatbot, text
from streamlit_chat import message
def main():

    st.set_page_config(page_title = 'Converse para seus aqruivos de texto', page_icon = ':books:')
    
    st.header('Converse com seus arquivos')
    user_question = st.text_input('Digite sua pergunta aqui')
    if('conversation' not in st.session_state):
        st.session_state.conversation = None
       
    if('session_id' not in st.session_state):
        st.session_state.session_id = None
    
    if user_question:
        message(user_question, key= str(0) + '_user', is_user=True)
        with st.spinner('Bot está respondendo...'):
            response = st.session_state.conversation.invoke({'input': user_question}, config={ "configurable": {"session_id": st.session_state.session_id}})
            message(response['answer'], key= str(1) + '_bot', is_user=False)
            for i, text_message in enumerate(response['chat_history']):
                if i % 2 == 0:
                 message(text_message.content, key= str(i+2) + '_user', is_user=True)  
                else:
                 message(text_message.content, key= str(i+2) + '_bot', is_user=False) 
            
        
       

    with st.sidebar:
        st.subheader('Seus arquivos')
        pdf_docs = st.file_uploader('Faça o upload de seus arquivos PDF', accept_multiple_files=True, type=['pdf'])
        session = st.text_input('Digite o ID da sessão')
        
        if st.button('Processar'):
           all_files_text = text.process_files(pdf_docs)
           chunks = text.crate_text_chunks(all_files_text)
           vectorstore = chatbot.create_vectorstore(chunks)
           st.session_state.conversation = chatbot.create_conversation_chain(vectorstore)
           st.session_state.session_id = session



if __name__ == '__main__':
    main()