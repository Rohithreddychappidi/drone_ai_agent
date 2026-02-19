from pydantic import BaseModel

class PilotUpdate(BaseModel):
    name: str
    status: str


class ChatRequest(BaseModel):
    query: str
