import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from genagent.utils.storages import BaseStorage


class JsonStorage(BaseStorage):

    def __init__(self, path: Optional[Path] = None) -> None:
        self.json_path = path
        self.json_path.touch()

    def save(self, records: List[Dict[str, Any]]) -> None:
        with self.json_path.open("a") as f:
            f.writelines([json.dumps(r, cls=json.JSONEncoder) + "\n" for r in records])

    def load(self) -> List[Dict[str, Any]]:
        with self.json_path.open("r") as f:
            return [json.loads(r) for r in f.readlines()]

    def clear(self) -> None:
        with self.json_path.open("w"):
            pass
