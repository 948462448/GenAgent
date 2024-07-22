from typing import List

from pydantic import BaseModel, Field

from genagent.assistant import BaseLLM
from genagent.memory import Message
from genagent.tool import BaseTool


class BaseAction(BaseModel):

    name: str = Field(default="")

    description: str = Field(default="")

    llm_model: BaseLLM = Field(default=None)

    message_list: List[Message] = Field(default_factory=List)

    prompt: str = Field(default="")

    tools: List[BaseTool] = Field(default_factory=List)

    def ask(self):
        pass

    def flush_memory(self):
        pass