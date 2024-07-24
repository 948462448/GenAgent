from typing import Optional, Union, Dict

from pydantic import BaseModel, Field, ConfigDict

from genagent.common.common_enum import ResponseStatusEnum


class Message(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    # id
    id: str = Field(default="")
    # Dialogue Content
    content: Union[str, Dict] = Field(default="")
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

    @staticmethod
    def do_format_message(content: str, role: str, name: str) -> str:
        return f'\\{"role":{role}, "content": {content}, "name":{name}\\}'

