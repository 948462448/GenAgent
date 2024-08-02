from abc import ABC, abstractmethod
from typing import List, Dict

from genagent.agent.agent import Agent
from genagent.assistant import llm_manager, BaseLLM
from genagent.memory.message import Message
from genagent.memory.shared_memory import SharedMemory


class BaseGroupExec(ABC):

    def __init__(self, **kwargs):
        self.llm: BaseLLM = llm_manager.create_llm_instance(kwargs.get("llm_config", None))
        self.shard_memory_list: SharedMemory = kwargs.get("shard_memory", SharedMemory())
        self.agents: Dict[str, Agent] = kwargs.get("agents", {})

    @abstractmethod
    def exec(self, message: Message, maximum_dialog_rounds: int = 10) -> None:
        """
        group exec
        :param message: new message
        :param maximum_dialog_rounds: maximum dialog rounds
        """
        pass




