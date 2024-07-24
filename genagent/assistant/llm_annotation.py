from genagent.common.common_enum import LLMProviderEnum
from genagent.assistant import llm_manager


def register_llm(llm_type: LLMProviderEnum):
    llm = llm_manager.LLM_MANGER

    def decorator(cls):
        llm.register(llm_type, cls)
        return cls

    return decorator
