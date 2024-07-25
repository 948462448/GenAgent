from abc import ABC, abstractmethod
from typing import Optional, List

from pydantic import BaseModel, Field


class Parameters(BaseModel):
    """
    param description
    """
    name: str = Field(default="")
    type: str = Field(default="string")
    description: str = Field(default="")
    enums: Optional[list[str]] = Field(default=None)
    required: bool = Field(default=False)


class BaseTool(ABC):

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def do_get_function_param(self) -> List[Parameters]:
        pass

    @abstractmethod
    def exec(self, **params):
        pass
