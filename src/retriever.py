# contains the search logic, responsible of answering user question
#1. load the vector database
#2. Check whether diversification is enabled
#embed the query
#compare with every stored vector
#return the top k
#retrieve more thn required
#reversify

from src.vectorstore import load_vectorstore
from src.config import Top_k

def retrieve(query, k=Top_k, diversify_sources=True, score_threshold=0.3):
    vectordb = load_vectorstore()

    # This returns a list of (Document, score) TUPLES — not Document objects directly
    raw_results_with_scores = vectordb.similarity_search_with_relevance_scores(query, k=k * 3)

    # Unpack each tuple into doc and score, keep only relevant ones
    relevant_results = []
    for item in raw_results_with_scores:
        doc, score = item          # <-- explicit unpacking, one tuple at a time
        if score >= score_threshold:
            relevant_results.append(doc)

    if not diversify_sources:
        return relevant_results[:k]

    seen_sources = set()
    diversified = []
    for doc in relevant_results:    # <-- doc here is now guaranteed to be a Document, not a tuple
        source = doc.metadata.get("source")
        if source not in seen_sources:
            diversified.append(doc)
            seen_sources.add(source)
        if len(diversified) >= k:
            break

    return diversified


