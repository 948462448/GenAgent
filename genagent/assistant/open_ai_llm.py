import json
from typing import List, Any, Union
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall

from genagent.assistant.base_llm import BaseLLM
from genagent.assistant.llm_config import LLMConfig
from genagent.assistant.llm_annotation import register_llm
from genagent.common import prompt_constant
from genagent.common.common_enum import LLMProviderEnum
from genagent.memory.message import Message


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
            presence_penalty=0.8,
            frequency_penalty=0.8,
            top_p=0.3,
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

    def request_function_call(self, messages: List[dict], tools: List[dict]) -> dict:
        """
        Whether the large language model chooses to invoke tools
        :param messages: chat message
        :param tools: tools
        :return: function name and params
        """
        # content = prompt_constant.ASSISTANT_CHOICE_TOOL_PROMPT_CN.format("{history}", json.dumps(messages))
        # messages = [Message.do_format_user_message(content, None)]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            stream=False
        )
        return response.choices[0].message.__dict__
