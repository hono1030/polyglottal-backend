from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from enum import Enum
from fastapi import FastAPI, HTTPException, Path, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from polyglottal_backend.routes.route import router, post_message
from pydantic import BaseModel
from typing import List
import json
import os
import uvicorn

load_dotenv()

app = FastAPI()

app.include_router(router)

print(os.getenv("FRONTEND_URL"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
            message = {"time": current_time, "clientId": client_id, "username": username, "message": data}
            try:
                await post_message(message)
                print("Message being added:", message)
            except Exception as e:
                print("Error posting message to MongoDB:", e)            
            await manager.broadcast(json.dumps(message))
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time": current_time, "clientId": client_id, "username": username, "message": f"{username} left the chat"}
        await manager.broadcast(json.dumps(message))


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("polyglottal_backend.main:app", port=8000, host="0.0.0.0", reload=True)

if __name__ == "main":
    start()
