from pydantic import BaseModel

class Message(BaseModel):
    time: str
    clientId: int
    username: str
    message: str
