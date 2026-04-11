from datetime import datetime
from anthropic.types import ToolParam

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty.")
    return datetime.now().strftime(date_format)


get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    "description": "Returns the current date and time formatted according to the specified format string. Use this tool whenever you need to know the current date or time.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "Python strftime format string. Defaults to '%Y-%m-%d %H:%M:%S'. Examples: '%Y-%m-%d' for date only, '%H:%M:%S' for time only, '%d/%m/%Y' for European format."
            }
        },
        "required": []
    }
})
