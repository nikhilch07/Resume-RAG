import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents", metadata={"hnsw:space":"cosine"})


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding

def add_chunks_to_db(chunks: list[str], source: str) -> None:
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.add(
            ids=[f"{source}_chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": source}]
        )

def search_similar(query: str, top_n: int = 3, source_filter: str | None = None) -> list[dict]:
    query_embedding = get_embedding(query)
    where_clause = {"source": source_filter} if source_filter else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n,
        where=where_clause
    )

    matches = []
    for text, distance in zip(results["documents"][0], results["distances"][0]):
        matches.append({"text": text, "distance": distance})
    return matches