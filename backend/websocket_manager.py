from fastapi import WebSocket
from typing import List
import json,redis,asyncio,os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
class ConnectionManager:
    def __init__(self):
        self.active_connections:List[WebSocket] = []
        self.redis_client = redis.from_url(REDIS_URL)
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe("incidents_channel")
    
    async def connect(self,websocket:WebSocket):

        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New WebSocket connection. Total: {len(self.active_connections)}")

    async def disconnect(self,websocket:WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self,message:dict):

        if not self.active_connections:
            return
        connections_copy = self.active_connections.copy()
        for connection in connections_copy:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Failed to send to client: {e}")
                self.disconnect(connection)

    async def listen_to_redis(self):
        """Listen for messages from Redis and broadcast to WebSocket clients"""

        print('Listening for redis messages')
        while True:
            try:
                message = self.pubsub.get_message(ignore_subscribe_messages=True)

                if message and message['type'] == 'message':
                    data = json.loads(message['data'])
                    print(f"📨 Received from Redis: {data['type']}")
                    await self.broadcast(data)
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error in Redis listener: {e}")
                await asyncio.sleep(1)
ws_manager = ConnectionManager()