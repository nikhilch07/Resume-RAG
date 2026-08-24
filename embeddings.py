import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")


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