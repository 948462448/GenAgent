from typing import List

from genagent.tool.base_tool import BaseTool, Parameters


class WeatherTool(BaseTool):
    @property
    def description(self) -> str:
        pass

    def do_get_function_param(self) -> List[Parameters]:
        pass

    def exec(self, **params):
        pass