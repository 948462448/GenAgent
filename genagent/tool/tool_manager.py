from typing import List, Dict

from genagent.tool.base_tool import BaseTool, Parameters


class Tool:
    def __init__(self, function_name: str, function_desc: dict, function_cls: BaseTool):
        self.function_name: str = function_name
        self.function_desc: dict = function_desc
        self.function_cls: BaseTool = function_cls

    def get_function_desc(self) -> dict:
        return self.function_desc

    def get_function_name(self) -> str:
        return self.function_name

    def get_function_cls(self) -> BaseTool:
        return self.function_cls


class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register_tool(self, tool: type):
        tool_instance = tool()
        tool_name = tool_instance.__class__.__name__
        parameters = tool_instance.do_get_function_param()
        function_desc = ToolManager.__format_function_desc(parameters, tool_name, tool_instance.description)
        self.tools[tool_name] = Tool(function_name=tool_name, function_desc=function_desc, function_cls=tool_instance)

    def get_tool(self, tool_name: str) -> Tool:
        return self.tools[tool_name]

    def __str__(self):
        tool_list = []
        for tool_name, tool_item in self.tools.items():
            tool_list.append(f"{tool_name}: {tool_item.function_desc}")
        return "\n".join(tool_list)

    @staticmethod
    def __format_function_desc(parameters: List[Parameters], tool_name: str, tool_desc: str):
        function_desc = {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_desc,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
        properties = {}
        required = []
        for param in parameters:
            property_dict = {
                "type": param.type,
                "description": param.description
            }
            if param.enums:
                property_dict["enum"] = param.enums
            if param.required:
                required.append(param.name)

            properties[param.name] = property_dict

        function_desc["function"]["parameters"]["properties"] = properties
        function_desc["function"]["parameters"]["required"] = required
        return function_desc


TOOL_MANAGER = ToolManager()
