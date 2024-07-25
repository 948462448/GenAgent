import json
from typing import Optional, Union, Dict

from pydantic import BaseModel, Field, ConfigDict

from genagent.common import prompt_constant
from genagent.common.common_enum import ResponseStatusEnum


class Message(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    # id
    id: str = Field(default="")
    # Dialogue Content
    content: Union[str, Dict[str, str]] = Field(default="")
    # Sender
    send_from: str = Field(default="")
    # Receiver agent_name
    send_to: str = Field(default="")
    # Send Time
    send_time: Optional[str] = Field(default=None)
    # response status
    status: str = Field(default=ResponseStatusEnum.SUCCESS.value)
    #
    role: str = Field(default="")

    def do_format_message(self, prompt: Optional[str]) -> dict:
        """
        Formatting the prompt passed to the LLM (Language Model).

        :param prompt: prompt
        :return: format message
        """
        chat = ""
        if prompt is None or prompt == "":
            chat = self.__do_format_msg_without_prompt(chat)
        else:
            chat = self.__do_format_msg_with_prompt(chat, prompt)
        return chat

    @staticmethod
    def do_format_system_message(content: str, name: str) -> dict:
        return {"role": "system", "content": content, "name": name}

    @staticmethod
    def do_format_agent_message(content: str, name: str) -> dict:
        return {"role": "assistant", "content": content, "name": name}

    @staticmethod
    def __do_check_placeholder_existence(prompt: str, placeholder: str):
        return f'{{{placeholder}}}' in prompt

    def __do_format_msg_with_prompt(self, chat, prompt):
        if isinstance(self.content, str):
            new_content = prompt + prompt_constant.USER_ASK_PROMPT_CN.format(content=self.content)
            chat = {"role": "user", "content": new_content, "name": self.send_from}
        else:
            new_content = prompt
            not_exists_dict = {}
            for key, value in self.content.items():
                if self.__do_check_placeholder_existence(prompt, key):
                    new_content = new_content.format(**{key: value})
                else:
                    not_exists_dict.pop(key, value)
            if len(not_exists_dict) > 0:
                dict_str = "\n".join([f'{key}: {value}' for key, value in not_exists_dict.items()])
                new_content = new_content + prompt_constant.USER_ASK_PROMPT_CN.format(content=dict_str)
            chat = {"role": "user", "content": new_content, "name": self.send_from}
        return chat

    def __do_format_msg_without_prompt(self, chat):
        if isinstance(self.content, str):
            chat = {"role": "user", "content": self.content, "name": self.send_from}
        elif isinstance(self.content, dict):
            dict_str = "\n".join([f'{key}: {value}' for key, value in self.content.items()])
            chat = {"role": "user", "content": dict_str, "name": self.send_from}
        return chat
