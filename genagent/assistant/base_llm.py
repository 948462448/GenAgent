from abc import ABC
from typing import List


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

class Foo(object): pass

subclasses = BaseLLM.__subclasses__()
for subclass in subclasses:
    print(subclass.__name__)