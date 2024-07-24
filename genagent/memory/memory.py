from abc import abstractmethod
from typing import List

from pydantic import BaseModel, Field

from genagent.memory.message import Message


class Memory(BaseModel):
    """ This is a basic memory model.  """

    # chat history list
    message_list: List[Message] = Field(default=[])

    @abstractmethod
    def save(self, key: Message) -> None:
        pass

    @abstractmethod
    def load(self) -> List[Message]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
