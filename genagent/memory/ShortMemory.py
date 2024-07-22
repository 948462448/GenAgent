from typing import Optional

from pydantic import BaseModel, Field

from genagent.memory import Memory
from genagent.utils.storages import BaseStorage, KeyValueStorage


class ShortMemory(BaseModel, Memory):
    """
    Short-term memory in computing refers to data stored in the system's main memory (RAM),
    which holds information temporarily for immediate access by the CPU.
    """

    storage: BaseStorage = Field(default_factory=KeyValueStorage)

    def get_memory(self):
        return self.storage.load()

    def persistence_memory(self):
        pass
