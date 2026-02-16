import os

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class JobRequest(BaseModel):
    job_title: str
    company_name: str
    job_description: str
    candidate_profile: str

@app.get("/")
def home():
    return {"message": "Ophias AI Job Engine is live 🚀"}

@app.post("/generate")
def generate_application(data: JobRequest):

    prompt = f"""
    You are a professional career assistant.

    Candidate Profile:
    {data.candidate_profile}

    Job Title: {data.job_title}
    Company: {data.company_name}

    Job Description:
    {data.job_description}

    1. Generate a tailored ATS-optimized CV.
    2. Generate a human-like professional cover letter.
    Make it natural, confident, and specific.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "result": response.choices[0].message.content
    }
