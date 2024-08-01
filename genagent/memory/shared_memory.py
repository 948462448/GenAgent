from copy import deepcopy
from typing import List

from pydantic import Field

from genagent.memory.memory import Memory
from genagent.memory.message import Message
from queue import Queue


class SharedMemory(Memory):

    shared_memory_max_size: int = Field(default=100)

    new_message_queue: Queue = Field(default=Queue(maxsize=shared_memory_max_size))

    def save(self, message: Message) -> None:
        self.message_list.append(message)

    def load(self) -> List[Message]:
        return deepcopy(self.message_list)

    def clear(self) -> None:
        self.message_list.clear()
