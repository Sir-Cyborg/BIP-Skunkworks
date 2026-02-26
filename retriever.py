import chromadb
from chromadb.utils import embedding_functions

class Retriever:
    def __init__(self, model_name="all-MiniLM-L6-v2", collection="policy_procedures"):
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")

        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name=collection,
            embedding_function=embedder
        )

    def retrieve(self, query, k=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        docs = results["documents"][0]
        metas = results["metadatas"][0]

        context_blocks = []
        for doc, meta in zip(docs, metas):
            header = (
                f"Source: {meta['original_file']} | "
                f"Section {meta['section_number']} {meta['section_title']}"
            )
            context_blocks.append(f"{header}\n{doc}")
        context = "\n\n".join(context_blocks)

        return context

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputQuery(BaseModel):
    query: str

@app.post("/retrieve")
def retrieve(input_query: InputQuery):
    retriever = Retriever()
    context = retriever.retrieve(input_query.query)
    return {"context": context}