from genagent.common.common_enum import GroupExecTypeEnum
from genagent.group import group_exec_manager


def register_group_exec(group_exec_type: GroupExecTypeEnum):
    exec_type = group_exec_manager.GROUP_EXEC_MANAGER

    def decorator(cls):
        exec_type.register(group_exec_type, cls)
        return cls

    return decorator
