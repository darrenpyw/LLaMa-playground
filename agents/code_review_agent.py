from ToolAgents.provider import OpenAIChatAPI
from ToolAgents.agents import ChatToolAgent
from ToolAgents.data_models.messages import ChatMessage
from ToolAgents.function_tool import ToolRegistry

from tools.tools import (
    timing_decorator,
    current_datetime_function_tool
)

@timing_decorator
def task(agent):
    um = ChatMessage.create_user_message("Analyze the file for security misconfigurations and write output to file with filename as '<current_timestamp>-<analyzed_filename>.md")
    um.add_text_file_data(file="..\\samples\\nginx.conf")
    
    messages = [
        ChatMessage.create_system_message("You are a cyber security expert in reviewing source code and infrastructure configurations with tool calling capabilities. Respond with professional tone and do not use emojis"),
        um,
    ]
    
    tools = [
        current_datetime_function_tool
    ]
    tool_registry = ToolRegistry()

    tool_registry.add_tools(tools)

    result = agent.get_streaming_response(
        messages=messages,
        tool_registry=tool_registry
    )

    for res in result:
        print(res.chunk, end='', flush=True)

def main():
    # Local OpenAI-compatible API, like vllm or llama-cpp-server
    api = OpenAIChatAPI(
        api_key="",
        base_url="http://127.0.0.1:8000/v1",
        model="unsloth/gemma-4-E2B-it-GGUF",
        )
    # Create the ChatAPIAgent
    agent = ChatToolAgent(chat_api=api)
    task(agent)

if __name__ == "__main__":
    main()