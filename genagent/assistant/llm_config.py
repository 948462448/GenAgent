from pydantic import Field, BaseModel

from genagent.common.common_enum import LLMProviderEnum


class LLMConfig(BaseModel):
    # LLM base config
    openai_api_key: str = Field(default="")
    openai_base_url: str = Field(default="")
    model: str = Field(default="")
    #
    llm_provider: LLMProviderEnum = Field(default=LLMProviderEnum.OPENAI)

    # todo add adding other parameters to the request for the large model


class DefaultLLMConfig(LLMConfig):
    # LLM base config
    openai_api_key: str = Field(default="sk-0da03bdfd5414766ae05a0050134cfb1")
    openai_base_url: str = Field(default="https://api.deepseek.com")
    model: str = Field(default="deepseek-chat")
    llm_provider: LLMProviderEnum = Field(default=LLMProviderEnum.OPENAI)
