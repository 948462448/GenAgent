import json
from typing import List

from pydantic import Field

from genagent.memory.memory import Memory
from genagent.memory.message import Message


class LongMemory(Memory):
    """ Persistent Memory """
    embedding_model: str = Field(default="")

    json_path: str = Field(default="")

    def save(self, records: List[Message]) -> None:
        with self.json_path.open("a") as f:
            f.writelines([json.dumps(r, cls=json.JSONEncoder) + "\n" for r in records])

    def load(self) -> List[Message]:
        with self.json_path.open("r") as f:
            return [json.loads(r) for r in f.readlines()]

    def clear(self) -> None:
        with self.json_path.open("w"):
            pass
