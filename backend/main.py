from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine,Base
from routes import logs
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(logs.router,prefix="/api")
@app.get("/")
def health():
    return {
        "message":"AI agent running"
    }
    
