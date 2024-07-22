from typing import Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    # id
    id: str = Field(default="")
    # Dialogue Content
    content: str = Field(default="")
    # Sender
    send_from: str = Field(default="")
    # Receiver
    send_to: str = Field(default="")
    # Send Time
    send_time: Optional[str] = Field(default=None)
    # Role
    role: str = Field(default="")
