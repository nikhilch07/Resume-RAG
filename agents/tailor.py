from core.client import client
from core.schema import Resume

def rewrite_resume_structured(original_text: str, jd_text: str, gaps: list[dict]) -> Resume:
    gap_summary = "\n".join([f"- {g['jd_requirement'][:100]}" for g in gaps if g["status"] == "GAP"])
    
    prompt = f"""Rewrite this resume to align with the job description, following strict rules:
1. NEVER invent skills or experience not present in the original.
2. Rephrase existing experience using JD terminology where genuinely applicable.
3. Return ONLY valid JSON matching this exact structure, nothing else:
4. Include ALL career highlights from the original resume — do not omit any website urls like linked profile url, github profile url.

{{
  "name": "...",
  "contact": "phone | email | location",
  "portfolio": "url or null",
  "summary": ["one or more summary sentences"],
  "skills": ["skill line 1", "skill line 2", ...],
  "career_highlights": ["highlight 1", "highlight 2", ...],
  "experience": [
    {{"job_title": "...", "company": "...", "location": "...", "tenure": "...", "bullets": ["...", "..."]}}
  ],
  "education": ["degree, school, year"]
}}

Original Resume:
{original_text}

Job Description:
{jd_text}

Gaps to be aware of (do not fabricate to fill these):
{gap_summary}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=2000
    )
    
    import json
    data = json.loads(response.choices[0].message.content)
    return Resume(**data)