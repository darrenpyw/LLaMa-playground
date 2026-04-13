import asyncio
import logging
import argparse
from pathlib import Path
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
def task(agent, settings, path):
    logging.debug(f"Processing file: {path}")

    um = ChatMessage.create_user_message(f"""
    Analyze the file {path} for security misconfigurations and output in markdown format with current timestamp.
    First, retrieve the current time in the format: %Y-%m-%d_%H-%M.
    Then write the analysis to a file named '<retrieved_timestamp>-<file_analyzed>.md' (replace <retrieved_timestamp> with the actual timestamp, replace <file_analyzed> with the actual filename analyzed).
    """)
    
    um.add_text_file_data(file=path)
    
    messages = [
        ChatMessage.create_system_message("""
            You are a cyber security expert in reviewing source code and infrastructure configurations with tool calling capabilities.
            Respond professionally and do not use emojis
            """),
        um,
    ]
    
    tools = [
        current_datetime_function_tool,
        write_file_tool
    ]

    tool_registry = ToolRegistry()

    tool_registry.add_tools(tools)
    
    result = agent.get_response(
        messages=messages,
        settings=settings,
        tool_registry=tool_registry
    )
    

@timing_decorator
async def main(args):
    # Local OpenAI-compatible API, like vllm or llama-cpp-server
    api = OpenAIChatAPI(
        api_key="",
        base_url="http://127.0.0.1:8000/v1",
        model="unsloth/gemma-4-E2B-it-GGUF",
        )
    
    settings = api.get_default_settings()

    # Set sampling settings
    settings.temperature = 1.0
    settings.top_p = 1.0

    # Create the ChatAPIAgent
    agent = ChatToolAgent(chat_api=api)
    
    # paths = ["..\\samples\\nginx.conf",
    #          "..\\samples\\app.py"
    #          ]
    
    paths = []

    if args.filename:
        paths.extend(args.filename)
    if args.directory:
        paths.extend([child for child in sorted(Path(args.directory).rglob('*')) if child.suffix in {".sol", ".py", ".conf", ".c", ".cpp", ".js", ".json"}])

    for path in paths:
        print(path)
    semaphore = asyncio.Semaphore(4)
    
    async def bounded_task(path):
        async with semaphore:
            await asyncio.to_thread(task, agent, settings, path)

    tasks = [bounded_task(path) for path in paths]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(filename=Path.cwd() / "output" / "runtime.log", format='%(asctime)s - %(funcName)s: %(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        prog = 'Asynchoronous Code Review Agent',
        description = 'Using LLM, review source codes for security issues'
        )
    parser.add_argument("filename", nargs='*', help="filename(s) to review")
    parser.add_argument("-d", "--directory", help="directory for recursively reviewing all files")
    args = parser.parse_args()
    if len(vars(args)) <= 0:
        parser.print_help()
    asyncio.run(main(args))