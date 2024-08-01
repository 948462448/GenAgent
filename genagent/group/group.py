from typing import List, Optional

from pydantic import BaseModel, Field

from genagent.agent.agent import Agent
from genagent.memory.shared_memory import SharedMemory


class Group(BaseModel):
    """
        workgroup
    """
    name: str = Field(default="")

    description: str = Field(default="")

    agents: List[Agent] = Field(default_factory=List)

    execType: str = Field(default="")  # ReAct / Order

    shard_memory_list: SharedMemory = Field(default_factory=SharedMemory)





