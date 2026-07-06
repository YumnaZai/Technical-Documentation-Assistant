#reads all docs, chunks them, embeds them, and writes the result
#slow  and only needs to run when your docs change
#re-run this whenever new documentation is added or existing docs are updated
import sys
sys.path.append(".")

from src.ingest import load_documents, chunk_documents
from src.vectorstore import build_vectorstore

print("Loading documents...")
docs = load_documents()
print(f"Loaded {len(docs)} documents")

print("Chunking...")
chunks = chunk_documents(docs)
print(f"Created {len(chunks)} chunks")

print("Building vector index...")
build_vectorstore(chunks)
print("Done! Vector DB saved to storage/vector_db")