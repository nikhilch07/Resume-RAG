# from client import client
from documents import load_pdf_text, chunk_text
from embeddings import add_chunks_to_db, search_similar
from matcher import analyze_gaps
from tailor import rewrite_resume_structured
from formatter import create_resume_docx


# response = client.chat.completions.create(
#     model = 'gpt-4o-mini',
#     messages=[
#         {"role": "user",
#          "content": "say hello in 5 words"
#          }
#     ]
# )

# print(response.choices[0].message.content)



# def embed_chunks(chunks: list[str]) -> list[dict]:
#     embedded = []
#     for chunk in chunks:
#         vector = get_embedding(chunk)
#         embedded.append({"text": chunk, "embedding": vector})
#     return embedded

# chunked_text = chunk_text(pdf_text, 50)

# vectorizing_embedding = embed_chunks(chunked_text)

# def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
#     vec1 = np.array(vec1)
#     vec2 = np.array(vec2)
#     return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# def find_relevant_chunks(question: str, embedded_chunks: list[dict], top_n: int = 3) -> list[str]:
#     question_embedding = get_embedding(question)

#     scored = []
#     for chunk in embedded_chunks:
#         score = cosine_similarity(question_embedding, chunk["embedding"])
#         scored.append((score, chunk["text"]))
    
#     scored.sort(reverse=True)
#     top_chunks = [ text for score, text in scored[:top_n]]
#     return top_chunks


resume_text = load_pdf_text("./resume.pdf")
chunks = chunk_text(resume_text, 50)
added_chunks_to_db = add_chunks_to_db(chunks, source="resume")

# results = search_similar("MCP experience", top_n = 1, source_filter="resume")
# print(results)


jd_text = """
BS in Computer Science or related area 

3+ years of software development experience.  

Strong foundation in computer science principles, including algorithms, data structures, and system design building scalable web applications and backend services 

Solid understanding of software engineering best practices, such as version control, testing, and continuous integration 

Java 

Spring 

NodeJS 

JavaScript/TypeScript 

At least one modern frontend framework (VueJS, React, or Angular) 

SQL and relational databases 

REST API 

Automated testing (JUnit, TestNG, Jest, Vitest, or similar) 

Familiarity with web technologies, APIs, and distributed systems 

Familiarity with Shift Left and test automation 

Effective communication skills and ability to work both independently and in a team 

Highly self-motivated with a strong sense of ownership; proactively identifies opportunities, takes initiative without being asked, and follows through with persistence. 

WHAT YOU'LL NEED

Preferred Requirements: 

Experience with generative AI, machine learning, and predictive algorithms 

Familiarity with statistics and healthcare domain 

Expertise with distributed event streaming platforms like Kafka  

Experience with data pipeline technologies 


"""

# bad_match = search_similar("experience with medieval blacksmithing", top_n=1, source_filter="resume")
# print(bad_match)

gaps = analyze_gaps(jd_text)

# for item in gaps:
#     print(f"[{item['status']}] (distance: {item['distance']}) — {item['jd_requirement'][:80]}...")


update_resume = rewrite_resume_structured(resume_text, jd_text, gaps)
print(f"UPDATED RESUME: {update_resume}")

create_resume_docx(update_resume, "tailored_resume.docx")


# def answer_question(question: str, embedded_chunks: list[dict]) -> str:
#     relevant_chunks = search_similar(question, embedded_chunks)
#     context = "\n\n".join(relevant_chunks)

#     prompt = f"""
# Answer the question based only on the context below. 
# If the answer isn't in the context, say you don't know.
#     Context: {context}
#     Question: {question} """

#     response = client.chat.completions.create(
#         model = "gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content

# def main():
#     print("Ask questions about document. Type 'exit' to quit. /n")

#     while True:
#         question = input("You: ")
        
#         if question.lower() == "exit":
#             print("Goodbye!")
#             break

#         answer = answer_question(question, added_chunks_to_db)
#         print(f"Answer: {answer} \n")

# if __name__ == "__main__":
#    main()