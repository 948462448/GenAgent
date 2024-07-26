from datetime import datetime
from typing import List

from genagent.tool.base_tool import BaseTool, Parameters
from genagent.tool.tool_annotation import register_tool


@register_tool
class CurrentDataTimeTool(BaseTool):
    @property
    def description(self) -> str:
        return "Get the current server's date and time."

    def do_get_function_param(self) -> List[Parameters]:
        date_format = Parameters(name="date_format", type="string",
                                 description="The output format string, defaulting to '%Y-%m-%d %H:%M:%S'.", )
        date_type = Parameters(name="date_type", type="string",
                                 description="The output time format can be one of the following options: date, time, or all. For example, when the value is 'date', the time is formatted as '2023-07-01'; when the value is 'time', it's formatted as '09:00:00'; and when the value is 'all', the time is formatted as '2023-07-01 09:00:00'.",
                                 enums=["date", "time", "all"])
        split_char = Parameters(name="split_char", type="string", description="The delimiter between date and time, which defaults to a space.")
        is_date_before = Parameters(name="is_date_before", type="string",
                                    description="True indicates that the date precedes the time, while False indicates that the date follows the time. The default is True. For example, with %H:%M:%S %Y-%m-%d, the value should be False.")
        return [date_format, date_type, split_char, is_date_before]

    def exec(self, date_format: str = "%Y-%m-%d %H:%M:%S", date_type: str = "all", split_char: str = " ",
             is_date_before: bool = True) -> dict:
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

        return {"current_data_time": current_time_str}
