from typing import List, Optional, Dict

from pydantic import Field, ConfigDict

from genagent.memory.memory import Memory
from genagent.memory.message import Message
from queue import Queue


class SharedMemory(Memory):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    shared_memory_max_size: int = Field(default=100)

    message_dict_group: dict[str, List[Message]] = Field(default={})

    new_message_queue: Queue = Field(default_factory=Queue)

    def save(self, message: Message) -> None:
        self.new_message_queue.put(message)
        self.message_list.append(message)
        if message.send_from not in self.message_dict_group:
            self.message_dict_group[message.send_from] = []
        self.message_dict_group[message.send_from].append(message)
        if message.send_to:
            if message.send_to not in self.message_dict_group:
                self.message_dict_group[message.send_to] = []
            self.message_dict_group[message.send_to].append(message)

    def load(self) -> List[Message]:
        return self.message_list

    def clear(self) -> None:
        self.message_list.clear()

    def get_message_by_send_from(self, send_from: str) -> Optional[List[Message]]:
        return self.message_dict_group.get(send_from, None)
