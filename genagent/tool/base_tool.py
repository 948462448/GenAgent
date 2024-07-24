from pydantic import BaseModel


class BaseTool(BaseModel):

    def get_function_desc(self):
        pass

    def exec(self):
        pass
