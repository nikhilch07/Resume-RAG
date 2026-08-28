from pypdf import PdfReader


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

pdf_text = load_pdf_text('./resume.pdf')
chunked_text = chunk_text(pdf_text, 50)
