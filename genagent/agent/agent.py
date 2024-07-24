from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field, ConfigDict

from genagent.assistant.base_llm import BaseLLM
from genagent.assistant import llm_manager
from genagent.common import prompt_constant
from genagent.common.common_enum import InteractionTypeEnum, ResponseStatusEnum, SendToTypeEnum
from genagent.memory.long_memory import LongMemory
from genagent.memory.message import Message
from genagent.memory.short_memory import ShortMemory
from genagent.tool.base_tool import BaseTool


class ExtendedParams(BaseModel):
    prompt_config: dict = Field(default=None)
    pass


class Agent(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    # agent name
    name: str = Field(default=None)
    # system prompt
    description: str = Field(default=None)
    # prompt
    prompt: str = Field(default="")
    # agent role
    role: str = Field(default="")
    # interaction type：human input / bot input
    interaction_type: str = Field(default=InteractionTypeEnum.MESSAGE.model_name)
    # agent short memory
    short_memory: ShortMemory = Field(default_factory=ShortMemory)
    # agent long memory
    long_memory: Optional[LongMemory] = Field(default=LongMemory)
    # agent tool
    tools: List[BaseTool] = Field(default=None)
    # extended params
    extended_params: Optional[ExtendedParams] = Field(default=None)
    # llm config
    llm: Optional[BaseLLM] = Field(default=None)

    """
        todo list
            1、接收消息 调用大模型
            2、更新短期记忆
            3、持久化到长期记忆
            4、tool的选择调度
    """

    def exec(self, message: Message) -> Message:
        if self.extended_params is not None and self.extended_params.prompt_config is not None:
            prompt_extend_config = self.extended_params.prompt_config["prompt"]
            self.prompt.format(**prompt_extend_config)
        new_content = self.__prompt_format(message)
        self.short_memory.save(message)
        response = self.__ask(message, new_content)
        self.short_memory.save(response)
        return response

    def __ask(self, message: Union[None, Message], new_content: str) -> 'Message':
        # 消息的构建
        if self.interaction_type == InteractionTypeEnum.HUMAN.model_name:
            """
            If the agent is human-input driven, simply return the output as is.
            """
            self.message = input(f"{self.name}: ")
            format_content = Message.do_format_message(self.message, self.role, self.name)
            msg = Message(content=format_content, send_from=self.name,
                          send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          status=ResponseStatusEnum.SUCCESS.value)
            return msg
        else:
            if message is None:
                msg = Message(content="The input message is empty, please re-enter.", send_from=self.name,
                              send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              status=ResponseStatusEnum.ERROR.value)
                return msg
            if self.llm is None:
                self.llm = llm_manager.create_llm_instance(None)

            if message.send_to != self.name and message.send_to != SendToTypeEnum.ALL.value:
                return Message(content="The message is not sent to this agent, ignore !", send_from=self.name,
                               send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               status=ResponseStatusEnum.ERROR.value)
            history_messages = self.short_memory.get_memory()
            history_messages_content = [message.content for message in history_messages]
            if self.description is not None:
                history_messages_content.insert(0, self.description)
            history_messages_content.append(new_content)
            response = self.llm.request(history_messages_content)
            return Message(content=response, send_from=self.name,
                           send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           status=ResponseStatusEnum.SUCCESS.value)

    def __prompt_format(self, message: Message) -> str:

        content = message.content
        if isinstance(content, dict):
            return self.prompt.format(**content)
        else:
            return self.prompt + prompt_constant.USER_ASK_PROMPT_CN.format(content=content)

    def __do_choice_tool(self, message: Message):
        pass

    def __do_execute_tool(self, tool: BaseTool, message: Message) -> 'Message':
        pass
