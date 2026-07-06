#Send retrieved chunks + question to the LLM, get back a natural-language answer with citations.

from openai import OpenAI
from src.config import OPENAI_API_KEY, llm_model 

#Convert the retrieved docs into context
#Build the user prompt
#system prompt

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a technical documentation assistant for a software company.
Answer the user's question using ONLY the provided context.
If the answer isn't in the context, say you don't have that information.
Cite the source file for each fact you state, like [source: auth-api.md]."""

def generate_answer(query, retrieved_docs):
    context_blocks = []
    for doc in retrieved_docs:
        source = doc.metadata.get("filename", "unknown")
        context_blocks.append(f"[Source: {source}]\n{doc.page_content}")

    context = "\n\n---\n\n".join(context_blocks)

    user_prompt = f"""Context:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model=llm_model ,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content