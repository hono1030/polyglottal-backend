from fastapi import FastAPI, HTTPException, Path, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
import uvicorn
from typing import List
from datetime import datetime
import json

# app = FastAPI(title="Polyglottal project")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# clients: List[WebSocket] = []

class ConnectionManager:
    def __init__(self):
        self.active__connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active__connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active__connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active__connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
def home():
    return "Hello World"

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            message = {"time": current_time, "clientId": client_id, "message": data}
            await manager.broadcast(json.dumps(message))
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time": current_time, "clientId": client_id, "message": "Offline"}
        await manager.broadcast(json.dumps(message))

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     clients.append(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             for client in clients:
#                 await client.send_text(f"Message text was: {data}")
#     except WebSocketDisconnect:
#         clients.remove(websocket)

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("polyglottal_backend.main:app", port=8000, reload=True)