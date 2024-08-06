from enum import Enum


class InteractionTypeEnum(Enum):
    """
    InteractionTypeEnum is an enum class that defines the different types of interactions that can be performed by an agent.
    """
    # The agent can interact with the world through human
    HUMAN = ("human", "human input")
    # The agent can interact with the world through a message.
    MESSAGE = ("message", "message input")

    @property
    def model_name(self):
        return self.value[0]

    @classmethod
    def get_enum_source_by_model_name(cls, model_name):
        if not model_name:
            return cls.MESSAGE
        for model_enum in cls:
            if model_enum.model_name == model_name:
                return model_enum
        return cls.MESSAGE


class LLMProviderEnum(Enum):
    """
    LLMTypeEnum is an enum class that defines the different types of LLMs that can be used by an agent.
    """
    # The agent can interact with the world through OpenAI
    OPENAI = "openai"


class ResponseStatusEnum(Enum):
    """
    ResponseTypeEnum is an enum class that defines the different types of responses that can be returned by an agent.
    """
    SUCCESS = "success"

    ERROR = "error"


class SendToTypeEnum(Enum):
    """
    SendToTypeEnum is an enum class that defines the different types of send to that can be used by an agent.
    """
    ALL = "all"
    ALL_MUTUALLY_EXCLUSIVE = "all_mutually_exclusive"
    ALL_NOT_MUTUALLY_EXCLUSIVE = "all_not_mutually_exclusive"


class GroupExecTypeEnum(Enum):
    """
    Types of Multi-Agent collaboration
    """
    REACT = "react"  # think -> act -> think -> act
    ORDER = "order"  # sequential execution
    CHAIN = "chain"  # specifying the next execution point
    PLAIN = "plain"  # LLM breaking down subtasks
    GRAPH = "graph"  # graph execution


class AgentExecModeEnum(Enum):
    """
    AgentExecModeEnum is an enum class that defines the different types of agent execution modes that can be used by an agent.
    """
    SIGNAL = "signal"
    MULTI = "multi"
