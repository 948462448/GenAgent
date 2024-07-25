from genagent.tool import tool_manager


def register_tool():
    tool = tool_manager.TOOL_MANAGER

    def decorator(cls):
        tool.register_tool(cls)
        return cls

    return decorator
