def set_reminder(content, timestamp):
  print(
    f"----\nSetting reminder for {timestamp}:\n{content}\n----\n"
    )

set_reminder_schema = {
    "name": "set_reminder",
    "description": "Sets a reminder with specific content at a given timestamp. Use this tool when the user wants to be reminded about something at a specific time or date.",
    "input_schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "The reminder message or content to display when the reminder triggers."
            },
            "timestamp": {
                "type": "string",
                "description": "The date and time when the reminder should trigger. Use ISO 8601 format: 'YYYY-MM-DDTHH:MM:SS'."
            }
        },
        "required": ["content", "timestamp"]
    }
}
