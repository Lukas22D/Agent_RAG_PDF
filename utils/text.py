from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
""" Módulo com funções para processamento de texto """

def process_files(files):
    """ Processa os arquivos PDF e retorna o texto extraído deles """
    text = ""
    for file in files:
        pdf = PdfReader(file)

        for page in pdf.pages:
            text += page.extract_text()
    
    return text

def crate_text_chunks(text):
    """ Divide o texto em chunks de 1000 caracteres """
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=300,
        length_function= len
    )

    chunks = text_splitter.split_text(text)
    return chunks