from pydantic import BaseModel, Field

from genagent.memory import Message


class Memory(BaseModel):
    """ This is a basic memory model.  """

    # chat history list
    message_list: list[Message] = Field(default=[])
