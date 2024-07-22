from copy import deepcopy
from typing import Any, List, Dict

from genagent.utils.storages import BaseStorage


class KeyValueStorage(BaseStorage):
    def __init__(self):
        self.key_value_list: List[Dict] = []

    def get_key_value_list(self) -> list:
        return self.key_value_list

    def save(self, key: list[dict[str, Any]]) -> None:
        self.key_value_list.extend(deepcopy(key))

    def load(self) -> list[dict[str, Any]]:
        return deepcopy(self.memory_list)

    def clear(self) -> None:
        self.key_value_list.clear()
