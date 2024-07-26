from genagent.tool import tool_manager


def register_tool(cls):
    tool_manager.TOOL_MANAGER.register_tool(cls)
    return cls
