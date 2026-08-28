from pydantic import BaseModel

class Experience(BaseModel):
    job_title: str
    company: str
    location: str
    tenure: str
    bullets: list[str]

class Resume(BaseModel):
    name: str
    contact: str
    portfolio: str | None = None
    summary: list[str]
    skills: list[str]
    career_highlights: list[str]
    experience: list[Experience]
    education: list[str]