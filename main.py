import os
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import numpy as np

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# response = client.chat.completions.create(
#     model = 'gpt-4o-mini',
#     messages=[
#         {"role": "user",
#          "content": "say hello in 5 words"
#          }
#     ]
# )

# print(response.choices[0].message.content)


def load_pdf_text(filepath: str) -> str:
    reader = PdfReader(filepath)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    
    return full_text


def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def embed_chunks(chunks: list[str]) -> list[dict]:
    embedded = []
    for chunk in chunks:
        vector = get_embedding(chunk)
        embedded.append({"text": chunk, "embedding": vector})
    return embedded

pdf_text = load_pdf_text('./resume.pdf')
chunked_text = chunk_text(pdf_text, 50)

vectorizing_embedding = embed_chunks(chunked_text)

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_relevant_chunks(question: str, embedded_chunks: list[dict], top_n: int = 3) -> list[str]:
    question_embedding = get_embedding(question)

    scored = []
    for chunk in embedded_chunks:
        score = cosine_similarity(question_embedding, chunk["embedding"])
        scored.append((score, chunk["text"]))
    
    scored.sort(reverse=True)
    top_chunks = [ text for score, text in scored[:top_n]]
    return top_chunks


def answer_question(question: str, embedded_chunks: list[dict]) -> str:
    relevant_chunks = find_relevant_chunks(question, embedded_chunks)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
Answer the question based only on the context below. 
If the answer isn't in the context, say you don't know.
    Context: {context}
    Question: {question} """

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def main():
    print("Ask questions about document. Type 'exit' to quit. /n")

    while True:
        question = input("You: ")
        
        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = answer_question(question, vectorizing_embedding)
        print(f"Answer: {answer} \n")

if __name__ == "__main__":
   main()