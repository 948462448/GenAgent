from copy import deepcopy
from typing import List

from pydantic import Field

from genagent.memory.memory import Memory
from genagent.memory.message import Message


class ShortMemory(Memory):
    """
    Short-term memory in computing refers to data stored in the system's main memory (RAM),
    which holds information temporarily for immediate access by the CPU.
    """
    # Longest memory limit
    memory_size: int = Field(default=100)

    # todo LRU 淘汰记忆

    def save(self, message: Message) -> None:
        self.message_list.append(message)

    def load(self) -> List[Message]:
        return deepcopy(self.message_list)

    def clear(self) -> None:
        self.message_list.clear()
