from typing import List

from pydantic import BaseModel, Field

from genagent.agent import BaseAgent
from genagent.memory import Memory


class BaseGroup(BaseModel):
    agents: List[BaseAgent] = Field(default_factory=List)

    execType: str = Field(default="")  # ReAct / Order

    shard_short_memory_list: List[Memory] = Field(default_factory=List)

