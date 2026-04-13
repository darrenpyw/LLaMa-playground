from ToolAgents.provider import OpenAIChatAPI
from ToolAgents.agents import ChatToolAgent
from ToolAgents.data_models.messages import ChatMessage
from ToolAgents.function_tool import ToolRegistry

from tools.tools import (
    timing_decorator,
    current_datetime_function_tool,
    write_file_tool
)

@timing_decorator
def task(agent, path):
    um = ChatMessage.create_user_message(f"""
    Analyze the file {path} for security misconfigurations and output in markdown format with current timestamp.
    First, retrieve the current time in the format: %Y-%m-%d_%H-%M.
    Then write the analysis to a file named '<retrieved_timestamp>-<file_analyzed>.md' (replace <retrieved_timestamp> with the actual timestamp, replace <file_analyzed> with the actual filename analyzed).
    """)
    um.add_text_file_data(file=path)
    
    messages = [
        ChatMessage.create_system_message("You are a cyber security expert in reviewing source code and infrastructure configurations with tool calling capabilities. Respond professionally and do not use emojis"),
        um,
    ]
    
    tools = [
        current_datetime_function_tool,
        write_file_tool
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

    paths = ["..\\samples\\nginx.conf",
             "..\\samples\\app.py"
             ]
    
    for path in paths:
        task(agent, path)

if __name__ == "__main__":
    main()