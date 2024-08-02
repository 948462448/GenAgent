import json
from datetime import datetime
from typing import List, Optional, Union, Dict, Tuple

from pydantic import BaseModel, Field, ConfigDict

from genagent.assistant import LLMConfig, BaseLLM
from genagent.assistant import llm_manager
from genagent.assistant.llm_config import DefaultLLMConfig
from genagent.common.common_enum import InteractionTypeEnum, ResponseStatusEnum, SendToTypeEnum, LLMProviderEnum
from genagent.memory.long_memory import LongMemory
from genagent.memory.message import Message
from genagent.memory.short_memory import ShortMemory
from genagent.tool import tool_manager


class ExtendedParams(BaseModel):
    prompt_config: dict = Field(default=None)
    max_react_num_of_cycle: int = Field(default=5)


class AgentTeam(BaseModel):
    team_name: str = Field(default="")
    team_role: str = Field(default="")


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
    # agent team
    team: List[AgentTeam] = Field(default=None)
    # interaction type：human input / bot input
    interaction_type: str = Field(default=InteractionTypeEnum.MESSAGE.model_name)
    # agent short memory
    short_memory: ShortMemory = Field(default_factory=ShortMemory)
    # agent long memory
    long_memory: Optional[LongMemory] = Field(default=LongMemory)
    # history messages
    history_messages: List[Dict] = Field(default=[])
    # agent tool
    tools: Optional[List[str]] = Field(default=None)
    # extended params
    extended_params: ExtendedParams = Field(default_factory=ExtendedParams)
    # llm config
    llm_config: Optional[LLMConfig] = Field(default_factory=DefaultLLMConfig)

    llm: Optional[BaseLLM] = Field(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm_manager.create_llm_instance(self.llm_config)

    """
        todo list
            3、持久化到长期记忆
    """
    def exec_group_agent(self, history_messages: List[Message], message: Message) -> Message:
        """
        Group-Agent Execution: Cooperative Execution with Other Agents
        """

        pass

    def exec_single_agent(self, message: Message) -> Message:
        """
        Single-Agent Execution: Direct execution without consideration of multi-agent coordination.
        """
        if self.extended_params.prompt_config is not None and len(self.extended_params.prompt_config) > 0:
            prompt_extend_config = self.extended_params.prompt_config["prompt"]
            self.prompt.format(**prompt_extend_config)
        self.short_memory.save(message)
        response = self.__ask(message)
        self.short_memory.save(response)
        return response

    def __ask(self, message: Union[None, Message]) -> 'Message':
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
            check_result, check_message = self.__check_message_relevant(message)
            if not check_result:
                return check_message
            if self.system_prompt is not None:
                self.history_messages.insert(0, Message.do_format_system_message(self.system_prompt, self.name))
            return self.__do_act(message)

    def __do_act(self, message: Message) -> 'Message':
        # By default, the system operates in React mode, whereas the implementation of the Order mode is yet to be added
        if self.tools is not None and len(self.tools) > 0:
            max_cycle = self.extended_params.max_react_num_of_cycle
            curr_cycle = 0
            new_content = message.do_format_message(self.prompt)
            self.history_messages.append(new_content)
            while curr_cycle < max_cycle:
                tools = self.__do_react_with_tool()
                if tools is None:
                    if curr_cycle == 0:
                        # On the first loop iteration, no tool match was found.
                        response = self.llm.request(self.history_messages)
                        return self.__do_init_message(content=response, send_to=message.send_from, is_success=True)
                    else:
                        # If it's not the first time, and it's determined that no tool is needed, then the most recent
                        # response from the latest historical conversation should suffice.
                        last_assistant_answer = self.history_messages[-1]
                        return self.__do_init_message(content=last_assistant_answer["content"],
                                                      send_to=message.send_from, is_success=True)
                self.__do_execute_tool(tools)
                response = self.llm.request(self.history_messages)
                self.history_messages.append(Message.do_format_agent_message(response, self.name))
                curr_cycle += 1
        else:
            new_content = message.do_format_message(self.prompt)
            self.history_messages.append(new_content)
            response = self.llm.request(self.history_messages)
            return self.__do_init_message(content=response, send_to=message.send_from, is_success=True)

    def __do_react_with_tool(self) -> 'Optional[List[Dict]]':
        """
        Utilize the React pattern, where the LLM autonomously determines which tools to use. This involves
        the model's self-selection of tools.
        """
        tool_manager_instance = tool_manager.TOOL_MANAGER
        if self.llm_config.llm_provider == LLMProviderEnum.OPENAI:
            # If the LLM type used by the current agent is OpenAI, then utilize the function_call capability of OpenAI.
            tool_desc_list = [tool_manager_instance.get_tool(tool_name=tool_name).get_function_desc() for tool_name in
                              self.tools]
            response = self.llm.request_function_call(messages=self.history_messages, tools=tool_desc_list)
            if response["tool_calls"] is None:
                return None
            self.history_messages.append(response)
            tools = []
            for tool_call in response["tool_calls"]:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                tools.append({"id": tool_call.id, "tool_name": tool_name, "tool_args": tool_args})
            return tools
        else:
            # todo 其他不是基于Openai模型的llm模型接入tool
            pass

    def __do_execute_tool(self, tools: List[dict]) -> None:
        for tool in tools:
            tool_name = tool["tool_name"]
            tool_args = tool["tool_args"]
            tool_instance = tool_manager.TOOL_MANAGER.get_tool(tool_name=tool_name)
            tool_response = tool_instance.get_function_cls().exec(**tool_args)
            self.history_messages.append({
                "tool_call_id": tool["id"],
                "role": "tool",
                "name": tool_name,
                "content": json.dumps(tool_response)
            })

    def __check_message_relevant(self, message: Message) -> Tuple[bool, Optional[Message]]:
        if message is None:
            return False, self.__do_init_message(content="The input message is empty, please re-enter.",
                                                 send_to=None, is_success=False)
        if message.send_to != self.name and message.send_to != SendToTypeEnum.ALL.value:
            return False, self.__do_init_message(content="The message is not sent to this agent, ignore !",
                                                 send_to=message.send_from, is_success=False)
        return True, None

    def __do_init_message(self, content: str, send_to: Optional[str], is_success: bool) -> 'Message':
        return Message(content=content, send_from=self.name, send_to=send_to,
                       send_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       status=ResponseStatusEnum.SUCCESS.value if is_success else ResponseStatusEnum.ERROR.value,
                       role=self.role)

    def to_dict(self):
        pass
