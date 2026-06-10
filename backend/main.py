from fastapi import FastAPI
from database import engine,Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
def health():
    return {
        "message":"AI agent running"
    }
    
