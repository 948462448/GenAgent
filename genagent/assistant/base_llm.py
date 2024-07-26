from abc import ABC
from typing import List, Dict


class BaseLLM(ABC):

    def request(self, messages: List) -> str:
        """
        Chat with LLM
        :param messages: chat message
        :return: LLM response
        """
        pass

    def request_stream(self, messages: List) -> str:
        """
        Stream chat with LLM
        :param messages: chat message
        :return: Stream LLM response
        """
        pass

    def request_function_call(self, messages: List[dict], tools: List[dict]) -> Dict:
        """
        Chat with LLM and get function call
        :param messages: chat message
        :param tools: tools
        :return: LLM response
        """
        pass
