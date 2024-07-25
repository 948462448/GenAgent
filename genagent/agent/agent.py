from datetime import datetime
from typing import List, Optional, Union, Dict

from pydantic import BaseModel, Field, ConfigDict

from genagent.assistant import LLMConfig
from genagent.assistant import llm_manager
from genagent.assistant.llm_config import DefaultLLMConfig
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
    # system prompt
    system_prompt: str = Field(default="")
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
    # history messages
    history_messages: List[Dict] = Field(default=[])
    # agent tool
    tools: List[BaseTool] = Field(default=None)
    # extended params
    extended_params: Optional[ExtendedParams] = Field(default=None)
    # llm config
    llm_config: Optional[LLMConfig] = Field(default_factory=DefaultLLMConfig)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm_manager.create_llm_instance(self.llm_config)

    """
        todo list
            3、持久化到长期记忆
            4、tool的选择调度
    """

    def exec(self, message: Message) -> Message:
        if self.extended_params is not None and self.extended_params.prompt_config is not None:
            prompt_extend_config = self.extended_params.prompt_config["prompt"]
            self.prompt.format(**prompt_extend_config)
        self.short_memory.save(message)
        response = self.__ask(message)
        self.short_memory.save(response)
        return response

    def __ask(self, message: Union[None, Message]) -> 'Message':
        # 消息的构建
        if self.interaction_type == InteractionTypeEnum.HUMAN.model_name:
            """
            If the agent is human-input driven, simply return the output as is.
            """
            self.message = input(f"{self.name}: ")
            format_content = message.do_format_agent_message(self.message, self.name)
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
            if message.send_to != self.name and message.send_to != SendToTypeEnum.ALL.value:
                return Message(content="The message is not sent to this agent, ignore !", send_from=self.name,
                               send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               status=ResponseStatusEnum.ERROR.value)
            if self.system_prompt is not None:
                self.history_messages.insert(0, Message.do_format_system_message(self.system_prompt, self.name))
            new_content = message.do_format_message(self.prompt)
            self.history_messages.append(new_content)
            response = self.llm.request(self.history_messages)
            return Message(content=response, send_from=self.name, send_to=message.send_from,
                           send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           status=ResponseStatusEnum.SUCCESS.value)

    def __do_choice_tool(self, message: Message):
        pass

    def __do_execute_tool(self, tool: BaseTool, message: Message) -> 'Message':
        pass

    def to_dict(self):
        pass
