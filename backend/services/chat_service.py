from sqlalchemy.orm import Session
from models import Log
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name="llama-3.3-70b-versatile",
)

def chat_with_logs(db:Session, question:str,user_id:str):

    recent_logs = db.query(Log).filter(Log.user_id == user_id).order_by(Log.timestamp.desc()).limit(100).all()

    logs_text = "\n".join([
        f"[{log.timestamp}] {log.level} - {log.service}: {log.message}"
        for log in recent_logs
    ])
    prompt = f"""You are an AI DevOps assistant. Answer the user's question based on these recent application logs.

LOGS:
{logs_text}

QUESTION: {question}

Provide a clear, concise answer based on the logs above. If the logs don't contain relevant information, say so."""
    response = llm.invoke(prompt)
    return response.content