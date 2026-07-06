#call both retriever.py then generator.py in sequence, packages the final result.

from src.retriever import retrieve
from src.generator import generate_answer

#works as ochestrator
#when user gives a answer_question
#the relevent chunks are retrieved
#if nothing found, the chnuks are are sent to LLM
#return nswer + source

refusal_phrase = ["i don't have that information",
    "i don't have information",
    "couldn't find anything relevant",]


def answer_question(query):
    retrieved_docs = retrieve(query)
    if not retrieved_docs:
        return  {"answer": "I couldn't find anything relevant in the documentation.",
                 "sources": [],
                }

    answer = generate_answer(query, retrieved_docs)

    is_refusal = any(phrase in answer.lower() for phrase in refusal_phrase)
    sources = [] if is_refusal else list({doc.metadata.get("filename") for doc in retrieved_docs})

    return {
        "answer": answer,
        "sources": sources,
    }


