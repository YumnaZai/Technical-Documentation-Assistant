#includes configuration infomation file paths, chunk size, model names, API keys

import os
from dotenv import load_dotenv # to laod var stored in .env

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

raw_docs_path = "data/raw_docs"
vector_db_path = "storage/vector_db"

chunk_size = 500 #recommended range for technical documents = 400-800
chunk_overlap = 50 # to prevent loass of meaning between chunks

embedding_model = "text-embedding-3-small"
llm_model =  "gpt-4o-mini" # based on reasoning ability and accuracy

Top_k = 5 # number of chunks to be retrieved
