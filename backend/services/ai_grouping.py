from langchain_groq import ChatGroq
from sqlalchemy.orm import Session
from models import Log
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()


#Load NLP model

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

llm = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name='llama3-8b-8192'
)

def cluster_logs(messages:list[str]):

    embeddings = embedding_model.encode(messages)

    clustering = DBSCAN(eps=0.5,min_samples=2,metric='cosine')
    labels = clustering.fit_predict(embeddings)
    
    return labels