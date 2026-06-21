from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from database import engine,Base
from routes import logs
from websocket_manager import ws_manager
import asyncio
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

@app.on_event("startup")
async def startup_event():
    """Start the Redis listener when FastAPI starts"""
    asyncio.create_task(ws_manager.listen_to_redis())
    print("🚀 WebSocket Redis listener started")

@app.websocket('/ws')
async def websocket_endpoint(websocket:WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

@app.get("/")
def health():
    return {
        "message":"AI agent running"
    }
    
