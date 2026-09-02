import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from core.documents import load_pdf_text, chunk_text
from rag.embeddings import add_chunks_to_db, search_similar, clear_resume_chunks
from rag.matcher import analyze_gaps
from agents.tailor import rewrite_resume_structured
from agents.formatter import create_resume_docx

app = FastAPI()


def cleanup_files(*paths: str) -> None:
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/tailor-resume")
async def tailor_resume(
    background_tasks: BackgroundTasks,
    resume_file: UploadFile,
    jd_text: str = Form(...)
):
    request_id = str(uuid.uuid4())
    temp_pdf_path = f"temp_{request_id}.pdf"
    output_path = f"tailored_resume_{request_id}.docx"

    try:
        # Basic file validation
        if not resume_file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        with open(temp_pdf_path, "wb") as f:
            shutil.copyfileobj(resume_file.file, f)

        resume_text = load_pdf_text(temp_pdf_path)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        chunks = chunk_text(resume_text, 50)

        clear_resume_chunks()
        add_chunks_to_db(chunks, source="resume")

        gaps = analyze_gaps(jd_text)
        resume_obj = rewrite_resume_structured(resume_text, jd_text, gaps)

        create_resume_docx(resume_obj, output_path)

    except HTTPException:
        cleanup_files(temp_pdf_path, output_path)
        raise
    except Exception as e:
        cleanup_files(temp_pdf_path, output_path)
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

    # schedule cleanup AFTER the file response has been sent
    background_tasks.add_task(cleanup_files, temp_pdf_path, output_path)

    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="tailored_resume.docx",
        background=background_tasks
    )