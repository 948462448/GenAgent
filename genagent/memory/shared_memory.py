from typing import List, Optional, Dict

from pydantic import Field

from genagent.memory.memory import Memory
from genagent.memory.message import Message
from queue import Queue


class SharedMemory(Memory):
    shared_memory_max_size: int = Field(default=100)

    message_dict_group: dict[str, List[Message]] = Field(default={})

    new_message_queue: Queue = Field(default=Queue(maxsize=shared_memory_max_size))

    def save(self, message: Message) -> None:
        self.message_list.append(message)
        send_message_list = self.message_dict_group.get(message.send_from, [])
        send_message_list.append(message)
        self.message_dict_group[message.send_from] = send_message_list

    def load(self) -> List[Message]:
        return self.message_list

    def clear(self) -> None:
        self.message_list.clear()

    def get_message_by_send_from(self, send_from: str) -> Optional[List[Message]]:
        return self.message_dict_group.get(send_from, None)
