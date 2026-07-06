#Wrap the embedding models
from langchain_openai import OpenAIEmbeddings
from src.config import embedding_model, OPENAI_API_KEY

def get_embedding_model():
    return OpenAIEmbeddings(model=embedding_model, api_key=OPENAI_API_KEY)