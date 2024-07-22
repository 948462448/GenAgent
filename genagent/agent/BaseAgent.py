from typing import List

from pydantic import BaseModel, Field

from genagent.actions import BaseAction
from genagent.memory import Memory


class BaseAgent(BaseModel):
    name: str = Field(default=None)
    description: str = Field(default=None)
    actions: List[BaseAction] = Field(default_factory=List)
    execType: str = Field(default="")  # ReAct / order
    short_memory: List[Memory] = Field(default_factory=List)
    long_memory: List[Memory] = Field(default_factory=List)
