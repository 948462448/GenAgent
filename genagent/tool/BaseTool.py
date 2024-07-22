from abc import ABC


class BaseTool(ABC):

    def get_function_desc(self):
        pass

    def exec(self):
        pass
