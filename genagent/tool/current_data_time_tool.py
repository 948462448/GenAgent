from datetime import datetime
from typing import List

from genagent.tool.base_tool import BaseTool, Parameters
from genagent.tool.tool_annotation import register_tool


@register_tool()
class CurrentDataTimeTool(BaseTool):
    @property
    def description(self) -> str:
        return "获取当前服务器的日期和时间"

    def do_get_function_param(self) -> List[Parameters]:
        date_format = Parameters(name="date_format", type="string",
                                 description="输出格式字符串，默认为'%Y-%m-%d %H:%M:%S'", )
        return_type = Parameters(name="date_type", type="string",
                                 description="输出时间类型，可选值为date、time或all，例如: 值为date的时候时间为 2023-07-01 值为 time 的时候时间为 09:00:00，值为 all 的时候时间为 2023-07-01 09:00:00",
                                 enums=["date", "time", "all"])
        split_char = Parameters(name="split_char", type="string", description="日期和时间之间的分隔符，默认为空格。")
        is_date_before = Parameters(name="is_date_before", type="string",
                                    description="True表示日期在时间之前，False表示日期在时间之后。默认为True。例如  %H:%M:%S %Y-%m-%d, 此时值应为false")
        return [date_format, return_type, split_char, is_date_before]

    def exec(self, date_format: str = "%Y-%m-%d %H:%M:%S", date_type: str = "all", split_char: str = " ",
             is_date_before: bool = True):
        """
        Get the current date or time, or both, according to the specified format.

        Parameters:

        date_format : str
           The output format string, default is '%Y-%m-%d %H:%M:%S'.
        return_type : str
           Possible values are 'date', 'time', or 'all'. Returns the date, time, or both respectively. Default is all.
        split_char : str
           The delimiter between date and time in date_format. Default is a space.
        is_date_before : bool
           True indicates the date comes before the time, False indicates the date comes after the time.

        Returns: str
            The formatted current date, time, or both.
        """
        current_datetime = datetime.now()
        if date_type == 'date':
            current_time_str = current_datetime.strftime(
                date_format.split(split_char)[0] if is_date_before else date_format.split(split_char)[1])
        elif date_type == 'time':
            current_time_str = current_datetime.strftime(
                date_format.split(split_char)[1] if is_date_before else date_format.split(split_char)[0])
        else:
            current_time_str = current_datetime.strftime(date_format)

        return f'{{ "current_data_time": "{current_time_str}"  }}'
