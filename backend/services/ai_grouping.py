from langchain_groq import ChatGroq
from sqlalchemy.orm import Session
from models import Log
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy as np
import os
from dotenv import load_dotenv
import re
import json
load_dotenv()


#Load NLP model

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

llm = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name='llama-3.3-70b-versatile'
)

def cluster_logs(messages:list[str]):

    embeddings = embedding_model.encode(messages)

    clustering = DBSCAN(eps=0.5,min_samples=2,metric='cosine')
    labels = clustering.fit_predict(embeddings)
    
    return labels

def summarize_cluster(messages:list[str]):
    sample = messages[:10]
    logs_text = "\n".join(sample)
    prompt = f"""You are an expert DevOps engineer analyzing application logs.
Here are some related error logs:

{logs_text}

Provide a JSON response with exactly these fields:
- group: short name for this issue
- summary: one sentence explanation of what went wrong
- severity: one of CRITICAL, HIGH, MEDIUM, LOW
- suggestion: one sentence on how to fix it

Return only raw JSON, no markdown, no backticks, no extra text."""
    
    response = llm.invoke(prompt)
    cleaned = re.sub(r'```json|```','',response.content).strip()
    try:
        return json.loads(cleaned)
    except:
        return {
            "raw":cleaned
        }

def group_and_summarise(db:Session):

    error_logs = db.query(Log).filter(Log.level == "ERROR").all()
    if not error_logs:
        return {
            "message":"no error logs found"
        }
    messages = [log.message for log in error_logs]

    labels = cluster_logs(messages)

    clusters = {}
    for i,label in enumerate(labels):
        if label == -1:
            continue
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(messages[i])
    
    results = []
    for label,msgs in clusters.items():
        summary = summarize_cluster(msgs)
        results.append({
            "cluster_id":int(label),
            "log_count":len(msgs),
            "ai_summary":summary
        })
    return results