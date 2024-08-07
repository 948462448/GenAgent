from typing import Optional

from genagent.assistant.llm_config import LLMConfig
from genagent.assistant.base_llm import BaseLLM

from genagent.assistant.llm_config import DefaultLLMConfig
from genagent.common.common_enum import LLMProviderEnum


class LLMManager:

    def __init__(self):
        self.llm_register = {}

    def register(self, llm_type: str, llm_class):
        self.llm_register[llm_type] = llm_class

    def get_llm(self, llm_type: str):
        return self.llm_register.get(llm_type)


def create_llm_instance(config: Optional[LLMConfig]) -> BaseLLM:
    """get the default llm provider"""
    if config is None:
        return LLM_MANGER.get_llm(llm_type=LLMProviderEnum.OPENAI.value)(DefaultLLMConfig())

    return LLM_MANGER.get_llm(llm_type=config.llm_provider)(config)


# Registry instance
LLM_MANGER = LLMManager()
