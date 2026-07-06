#Reads files off disk, splits them into chunks, attaches metadata

import os
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from src.config import raw_docs_path,chunk_size ,chunk_overlap

#load the documents
#load the documents
# scan documants
#get the files in the folder
#filter the useful files
#read file content
#attach metadata

def load_documents(base_path=raw_docs_path):

    documents = []
    for root, _, files in os.walk(base_path): #scan documants
        for file in files: #get the files in the folder
            if file.endswith((".md", ".txt")): #filter the useful files
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:  #read the file content
                    text = f.read()

                # Category = the subfolder name
                category = os.path.relpath(root, base_path).split(os.sep)[0] # attach metadata

                documents.append({ # stor the document
                    "text": text,
                    "source": filepath,
                    "filename": file,
                    "category": category,
                })
    return documents


#devide into chunks
def chunk_documents(documents):
    """Split each document into overlapping chunks, preserving metadata."""

    #split on markdown headers first to keep sections intact
    headers_to_split_on = [("#", "H1"), ("##", "H2"), ("###", "H3")]
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    #Further split large sections by character count
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    all_chunks = []
    for doc in documents:
        header_chunks = header_splitter.split_text(doc["text"]) # header splitting
        for hc in header_chunks:
            sub_chunks = char_splitter.split_text(hc.page_content) # spolit characters in each section
            for sc in sub_chunks:
                all_chunks.append({
                    "text": sc,
                    "metadata": {
                        "source": doc["source"],
                        "filename": doc["filename"],
                        "category": doc["category"],
                        "section": hc.metadata.get("H2") or hc.metadata.get("H1") or "General",
                    }
                })
    return all_chunks





