from pydantic import Field, BaseModel

from genagent.common.common_enum import LLMProviderEnum


class LLMConfig(BaseModel):
    # LLM base config
    openai_api_key: str = Field(default="")
    openai_base_url: str = Field(default="")
    model: str = Field(default="")
    #
    llm_provider: str = Field(default=LLMProviderEnum.OPENAI.value)
    temperature: float = Field(default=0.0)
    frequency_penalty: float = Field(default=0.0)
    presence_penalty: float = Field(default=0.0)
    is_json: bool = Field(default=False)
    # todo add adding other parameters to the request for the large model


class DefaultLLMConfig(LLMConfig):
    # LLM base config
    openai_api_key: str = Field(default="sk-0da03bdfd5414766ae05a0050134cfb1")
    openai_base_url: str = Field(default="https://api.deepseek.com")
    model: str = Field(default="deepseek-chat")
    llm_provider: str = Field(default=LLMProviderEnum.OPENAI.value)
