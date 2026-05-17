import json
import os
from pydantic import BaseModel
from google import genai
from google.genai import types

class StudyWeek(BaseModel):
    week: int
    focus: str
    tasks: list[str]
    btk_topics: list[str]

class PilotResponse(BaseModel):
    summary: str
    timeline: list[StudyWeek]
    project_name: str
    project_details: str

def generate_roadmap(career, current, missing, archetype):
    # Professional decoupled memory extraction
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Runtime Error: GEMINI_API_KEY variable is missing from system memory.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Analyze this student profile and output a 4-week study plan.
    Persona: {archetype}
    Goal: {career}
    Current: {', '.join(current) if current else 'None'}
    Gaps: {', '.join(missing)}
    """

    resp = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PilotResponse,
            temperature=0.7
        )
    )

    return json.loads(resp.text)