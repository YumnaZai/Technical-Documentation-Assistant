#Handles saving/loading the vector database 
from langchain_community.vectorstores import Chroma
from src.embed import get_embedding_model
from src.config import vector_db_path
#1. extract the text
#2. extract meta data seperately
#3. what chroma does -
# take a chunk until all chunks have an embedding
#store chunk text + embedding+ metadata to a database and in to disk
#return the vector database as a object

def build_vectorstore(chunks):
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    embedding_model = get_embedding_model()
    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas,
        persist_directory=vector_db_path,
    )
    vectordb.persist()
    return vectordb

#1. reopen the existing db
def load_vectorstore():
    embedding_model = get_embedding_model()
    return Chroma(
        persist_directory=vector_db_path,
        embedding_function=embedding_model,
    )