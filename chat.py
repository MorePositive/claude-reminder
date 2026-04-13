import time
from anthropic import Anthropic, APIStatusError
from anthropic.types import Message
from dotenv import load_dotenv
import json
# Import tool schemas and implementations
from tools.add_duration_to_datetime import add_duration_to_datetime_schema
from tools.add_duration_to_datetime import add_duration_to_datetime
from tools.get_current_datetime import get_current_datetime_schema
from tools.get_current_datetime import get_current_datetime
from tools.set_reminder import set_reminder_schema
from tools.set_reminder import set_reminder

load_dotenv()

client = Anthropic()

def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(user_message)

def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(assistant_message)

def chat(
  messages,
  system=None,
  temperature=1.0,
  stop_sequences=[],
  tools=None
  ):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 200,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
        "tools": tools
    }

    if system:
        params["system"] = system
    
    if tools:
        params["tools"] = tools
    
    for attempt in range(3):
        try:
            return client.messages.create(**params)
        except APIStatusError as e:
            if e.status_code == 529 and attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise

def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )

def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_input)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

def run_tools(response):
    tool_requests = [
        block for block in response.content if block.type == "tool_use"
    ]
    tool_result_blocks = []
    for tool_request in tool_requests:
        try:
          tool_output = run_tool(tool_request.name, tool_request.input)
          tool_result_block = {
              "type": "tool_result",
              "tool_use_id": tool_request.id,
              "content": json.dumps(tool_output),
              "is_error": False
          }
          tool_result_blocks.append(tool_result_block)
        except Exception as e:
          tool_result_block = {
              "type": "tool_result",
              "tool_use_id": tool_output.id,
              "content": f"Error: {e}",
              "is_error": True
          }
          tool_result_blocks.append(tool_result_block)
            
    return tool_result_blocks

def run_conversation(messages):
    while True:
        response = chat(messages=messages, tools=[
            get_current_datetime_schema,
            add_duration_to_datetime_schema,
            set_reminder_schema
            ])

        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break
        
        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages

messages = []

add_user_message(messages, "Set a reminder for me to get the car from the service station in 5 days")

run_conversation(messages)

