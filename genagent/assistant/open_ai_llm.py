from typing import List

from openai import OpenAI

from genagent.assistant.base_llm import BaseLLM, Foo
from genagent.assistant.llm_config import LLMConfig
from genagent.assistant.llm_annotation import register_llm
from genagent.common.common_enum import LLMProviderEnum

class Bar(Foo): pass



@register_llm(LLMProviderEnum.OPENAI)
class OpenAILLM(BaseLLM):
    """
    All LLMs that are compatible with OpenAI can use this configuration.
    """

    def __init__(self, config: LLMConfig):
        self.client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
        self.model = config.model

    def request(self, messages: List) -> str:
        """
        Chat with LLM
        :param messages: chat message
        :return: LLM response
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content

    def request_stream(self, messages: List) -> str:
        """
       Stream chat with LLM
       :param messages: chat message
       :return: Stream LLM response
       """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        model_answer_messages = []
        for chunk in response:
            chunk_message = chunk.choices[0].delta.content  # extract the message
            model_answer_messages.append(chunk_message)  # save the message
            yield chunk_message

print([cls.__name__ for cls in BaseLLM.__subclasses__()])