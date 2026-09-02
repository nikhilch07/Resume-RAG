from core.langchain_client import llm
from core.schema import JobInfo

def extract_job_info(job_text: str) -> JobInfo:
    structured_llm = llm.with_structured_output(JobInfo)
    return structured_llm.invoke("Extract job info from this posting: " + job_text)

result = extract_job_info("We are unable to sponsor visas for this role.")
print(result)