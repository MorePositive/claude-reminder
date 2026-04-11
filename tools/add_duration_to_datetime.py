from datetime import datetime, timedelta

def add_duration_to_datetime(datetime_str, duration=0, unit="days", input_format="%Y-%m-%d"):
  date = datetime.strptime(datetime_str, input_format)

  if unit == "seconds":
    date += timedelta(seconds=duration)
  elif unit == "minutes":
    date += timedelta(minutes=duration)
  elif unit == "hours":
    date += timedelta(hours=duration)
  elif unit == "days":
    date += timedelta(days=duration)
  elif unit == "weeks":
    date += timedelta(weeks=duration)
  elif unit == "months":
    month = date.month + duration
    year = date.year + month // 12
    month = month % 12
    if month == 0:
      month = 12
      year -= 1
    day = min(date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    date = date.replace(year=year, month=month, day=day)
  elif unit == "years":
    date = date.replace(year=date.year + duration)
  else:
    raise ValueError(f"Unsupported time unit: {unit}")
  
  return date.strftime("%A, %B %d, %Y at %I:%M %p")

add_duration_to_datetime_schema = {
    "name": "add_duration_to_datetime",
    "description": "Adds a duration to a given datetime string and returns the resulting date formatted as a human-readable string (e.g. 'Monday, April 10, 2026 at 12:00 PM'). Use this when the user asks about a future or past date relative to a given starting point.",
    "input_schema": {
        "type": "object",
        "properties": {
            "datetime_str": {
                "type": "string",
                "description": "The starting date/time string to add duration to. Must match the input_format. Example: '2026-04-10'."
            },
            "duration": {
                "type": "number",
                "description": "The amount of time to add. Can be negative to subtract time. Defaults to 0."
            },
            "unit": {
                "type": "string",
                "enum": ["seconds", "minutes", "hours", "days", "weeks", "months", "years"],
                "description": "The unit of time for the duration. Defaults to 'days'."
            },
            "input_format": {
                "type": "string",
                "description": "Python strftime format string for parsing datetime_str. Defaults to '%Y-%m-%d'. Example: '%Y-%m-%d %H:%M:%S' for datetime with time."
            }
        },
        "required": ["datetime_str"]
    }
}
