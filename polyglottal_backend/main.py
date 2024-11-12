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

class Userdata(BaseModel):
    username: str

@app.get("/")
def home():
    return "Hello World"

@app.post("/login")
def create_userdata(userdata: Userdata) -> dict[str, str]:
    print(userdata)
    # username = userdata.username
    
    return {"username": userdata.username}
    

@app.websocket("/ws/{username}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, username: str, client_id: int):
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            message = {"time": current_time, "clientId": client_id, "username": username, "message": data} # might change to the other tutorial one
            await manager.broadcast(json.dumps(message))
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time": current_time, "clientId": client_id, "username": username, "message": f"{username} left the chat"} # might change to the other tutorial one
        await manager.broadcast(json.dumps(message))


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("polyglottal_backend.main:app", port=8000, host="0.0.0.0", reload=True)