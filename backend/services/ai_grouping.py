from langchain_groq import ChatGroq
from sqlalchemy.orm import Session
from models import Log
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def group_and_summarise(db: Session,user_id:str):
    # Get only ERROR logs
    error_logs = db.query(Log).filter(Log.user_id == user_id).all()

    if not error_logs:
        return {"message": "no error logs found"}

    # Prepare log text
    logs_text = "\n".join([
        f"{log.service}: {log.message}"
        for log in error_logs[:200]  # limit to 200 logs
    ])

    prompt = f"""You are an expert DevOps engineer analyzing application error logs.

Here are {len(error_logs)} error logs:

{logs_text}

Group similar logs by root cause. Return ONLY a JSON array like this:
[
  {{
    "cluster_id": 0,
    "log_count": 50,
    "ai_summary": {{
      "group": "Short group name",
      "summary": "One sentence explanation",
      "severity": "CRITICAL",
      "suggestion": "One sentence fix suggestion"
    }}
  }}
]

Severity must be one of: CRITICAL, HIGH, MEDIUM, LOW
Return only raw JSON array, no markdown, no backticks."""

    response = llm.invoke(prompt)
    
    try:
        cleaned = re.sub(r'```json|```', '', response.content).strip()
        return json.loads(cleaned)
    except:
        return {"message": "Failed to parse AI response"}