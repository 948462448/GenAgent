from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def save(self, key: list[dict[str, Any]]) -> None:
        pass

    @abstractmethod
    def load(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
