from typing import Any

from pydantic import BaseModel, Field

from genagent.memory import Memory
from genagent.utils.storages import BaseStorage, JsonStorage


class LongMemory(BaseModel, Memory):
    """ Persistent Memory """

    embedding_model: str = Field(default="")

    storage: BaseStorage = Field(default_factory=JsonStorage)

    def get_memory(self) -> list[dict[str, Any]]:
        return self.storage.load()

    def save_memory(self, records: list[dict[str, Any]]) -> None:
        self.storage.save(records)

