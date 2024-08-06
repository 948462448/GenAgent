from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from genagent.agent.agent import Agent
from genagent.assistant import LLMConfig
from genagent.common.common_enum import GroupExecTypeEnum
from genagent.common.common_exception import ServerException, ErrorCode
from genagent.group import group_exec_manager
from genagent.memory.message import Message
from genagent.memory.shared_memory import SharedMemory


class Group(BaseModel):
    """
        workgroup
    """
    name: str = Field(default="")

    description: str = Field(default="")

    agents: Dict[str, Agent] = Field(default={})

    execType: GroupExecTypeEnum = Field(default=GroupExecTypeEnum.REACT)  # ReAct / Order / Chain / Plan / Graph

    shard_memory: SharedMemory = Field(default_factory=SharedMemory)

    finsh_flag: str = Field(default="")

    maximum_dialog_rounds: int = Field(default=10)

    llm_config: Optional[LLMConfig] = Field(default=None)

    def run(self, message: Message):
        """
        run group
        """
        if len(self.agents) == 0:
            return
        check_res = self.__check_agent_config()
        if not check_res:
            # todo log and error throw
            return
        group_exec_cls = group_exec_manager.GROUP_EXEC_MANAGER.get_exec_cls(exec_type=self.execType)
        if group_exec_cls:
            group_exec_instance = group_exec_cls(agents=self.agents, llm_config=self.llm_config, shard_memory=self.shard_memory)
            group_exec_instance.exec(message=message, maximum_dialog_rounds=self.maximum_dialog_rounds)
        else:
            raise ServerException(error_enum=ErrorCode.GROUP_EXEC_TYPE_NOT_SUPPORT_ERROR)

    def add_group(self, agent: Agent) -> None:
        self.agents[agent.name] = agent

    def __check_agent_config(self) -> bool:
        return True
