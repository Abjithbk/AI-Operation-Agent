from fastapi import FastAPI
from database import engine,Base
from routes import logs
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(logs.router,prefix="/api")
@app.get("/")
def health():
    return {
        "message":"AI agent running"
    }
    
