from enum import Enum
from typing import Optional


class CommonException(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
        super().__init__(f"error_code: {self.error_code}, error_msg: {self.message}")


class AgentException(CommonException):
    pass


class ServerException(CommonException):
    def __init__(self, **kwargs):
        self.error_enum: Optional[ErrorCode] = kwargs.get('error_enum', None)
        if not self.error_enum:
            self.error_code = kwargs.get('error_code', "")
            self.message = kwargs.get('error_msg', "")
        else:
            self.error_code = self.error_enum.code
            self.message = self.error_enum.errmsg

        super().__init__(self.error_code, self.message)


class ErrorCode(Enum):
    SERVER_ERR = ("500", '服务器异常')
    # 0000 common error
    REQUEST_TYPE_NO_SUPPORT_ERROR = ("0000001", "The request protocol is not supported")
    QUERY_DATA_NO_EXISTS_ERROR = ("0000002", "Data not found")
    PARAMS_EMPTY_ERROR = ("0000003", "Parameter is empty:{param_name}")
    ENUM_NOT_FIND_ERROR = ("0000004", "No matching enumeration found:{enum_name}")

    # 0001 group error
    GROUP_EXEC_TYPE_NOT_SUPPORT_ERROR = ("0001001", "Unsupported group execution type:{exec_type}")
    GROUP_AGENTS_EMPTY_ERROR = ("0001002", "The Group's Agents are Empty")
    GROUP_AGENTS_NOT_FOUNT_ERROR = ("0001003", "The agent is not found")

    @property
    def code(self):
        """get status code"""
        return self.value[0]

    @property
    def errmsg(self, **kwargs):
        """retrieve status code information"""
        return self.value[1].format(**kwargs)

    @property
    def error_print(self, **kwargs):
        error = {
            "code": self.code,
            "msg": self.errmsg.format(**kwargs),
            "success": True if self.code == "200" else False
        }
        return error
