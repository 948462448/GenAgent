import json
from typing import Optional

from genagent.common import prompt_constant
from genagent.common.common_enum import GroupExecTypeEnum
from genagent.common.common_exception import ServerException, ErrorCode
from genagent.group.base_group_exec import BaseGroupExec
from genagent.group.group_exec_annotation import register_group_exec
from genagent.memory.message import Message


@register_group_exec(GroupExecTypeEnum.REACT)
class GroupExecReact(BaseGroupExec):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exec(self, message: Message, maximum_dialog_rounds: int = 10) -> None:
        curr_round = 0
        while curr_round < maximum_dialog_rounds:
            self.shard_memory_list.new_message_queue.get()
            _react_message = self._react(message=message)
            if _react_message is not None:
                self.shard_memory_list.message_list.append(_react_message)
                self.shard_memory_list.message_dict_group[_react_message.send_from].append(_react_message)
                self.shard_memory_list.new_message_queue.put(_react_message)
            else:
                print("---------- Complete the conversation ----------")
                return
            curr_round += 1
        print("---------- Maximum conversation limit reached ----------")

    def _react(self, message: Message) -> Optional[Message]:
        if not self.agents:
            raise ServerException(error_enum=ErrorCode.GROUP_AGENTS_EMPTY_ERROR)
        send_to = message.send_to
        send_from_messages = self.shard_memory_list.message_dict_group.get(message.send_from)
        if send_to:
            if send_to in self.agents.keys():
                message = self.agents.get(send_to).exec_group_agent(history_messages=send_from_messages,
                                                                    message=message)
                return message
            else:
                raise ServerException(error_enum=ErrorCode.GROUP_AGENTS_NOT_FOUNT_ERROR)
        else:
            agent_desc_list = [{"agent_name": agent.name, "desc": agent.description} for agent in self.agents]
            history_messages_list = [message.do_format_message(prompt=None) for message in
                                     self.shard_memory_list.message_list]
            new_message = message.do_format_message(prompt=None)
            group_choice_prompt = prompt_constant.GROUP_CHOICE_AGENT_PROMPT_CN.format(agents=agent_desc_list,
                                                                                      history_messages=history_messages_list,
                                                                                      new_message=new_message)
            choice_messages = [
                Message.do_format_system_message(content=prompt_constant.GROUP_CHOICE_SYSTEM_PROMPT_CN, name="system"),
                Message.do_format_user_message(content=group_choice_prompt, name=None)]
            llm_response = self.llm.request(messages=choice_messages)
            next_agent_dict = json.loads(llm_response)
            next_agent_name = next_agent_dict.get("agent_name")
            if "None" == next_agent_name:
                return None
            new_answer_message = self.agents.get(next_agent_name).exec_group_agent(history_messages=send_from_messages,
                                                                                   message=message)
            return new_answer_message
