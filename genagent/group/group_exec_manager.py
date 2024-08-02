from genagent.common.common_enum import GroupExecTypeEnum
from genagent.group import BaseGroupExec


class GroupExecManager:
    def __init__(self):
        self.group_exec_type = {}

    def register(self, exec_type: GroupExecTypeEnum, group_exec_cls) -> None:
        self.group_exec_type[exec_type] = group_exec_cls

    def get_exec_cls(self, exec_type: GroupExecTypeEnum) -> BaseGroupExec:
        return self.group_exec_type.get(exec_type)


# Registry instance
GROUP_EXEC_MANAGER = GroupExecManager()
