from abc import ABC

from pydantic import Field


class BaseLLM(ABC):

    openai_api_key: str = Field(default="")

    openai_base_url: str = Field(default="")

    model: str = Field(default="deepseek-chat")

    stream: bool = Field(default=False)

