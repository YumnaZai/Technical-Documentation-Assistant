#to check automaically if the retriever logic works
import sys
sys.path.append(".")
from src.retriever import retrieve

def test_multi_document_retrieval():
    results = retrieve("How do refresh tokens work?")
    sources = {doc.metadata["source"] for doc in results}
    assert len(sources) > 1, "Expected retrieval to span multiple source documents"
    print("Sources retrieved:", sources)

test_multi_document_retrieval()