from typing import List, Optional

from pydantic import BaseModel, Field

from genagent.agent import agent
from genagent.memory import memory, message


class Group(BaseModel):
    """
        workgroup
    """
    agents: List[Agent] = Field(default_factory=List)

    execType: str = Field(default="")  # ReAct / Order

    shard_short_memory_list: List[Memory] = Field(default_factory=List)

    last_message: Optional[Message] = Field(default=None)

