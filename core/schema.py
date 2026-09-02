from pydantic import BaseModel, Field

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

class JobInfo(BaseModel):
    title: str | None = Field(default=None, description="The job title, if stated in the posting")
    visa_sponsorship_mentioned: bool = Field(description="True if the posting explicitly addresses visa sponsorship, either way")
    sponsorship_detail: str = Field(default="", description="Quote or paraphrase the exact sponsorship language if present, else empty string")
    location: str | None = Field(default=None, description="Job location if stated, else null")
    experience_level: str | None = Field(default=None, description="e.g. entry, mid, senior — if stated, else null")