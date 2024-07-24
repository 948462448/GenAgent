from typing import List

from pydantic import BaseModel, Field

from genagent.assistant import base_llm
from genagent.memory import message
from genagent.tool import base_tool


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