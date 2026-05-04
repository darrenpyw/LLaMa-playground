import asyncio
import logging
import argparse
import sys
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

    with open("./skills/C-Code_Reviewer simplified.md", "r") as f:
        sm = ChatMessage.create_system_message(f.read())
    
    um = ChatMessage.create_user_message(f"""
    Analyze the attached file {path} for security vulnerabilities and misconfigurations.
    
    The file content is delimited between <FILE_CONTENT_START> and <FILE_CONTENT_END>.
    First, retrieve the current time in the format: %Y-%m-%d_%H-%M.
    Then write the analysis to a file named '<retrieved_timestamp>-<file_analyzed>.md' (replace <retrieved_timestamp> with the actual timestamp, replace <file_analyzed> with the actual filename).
    """)
    
    um.add_text_file_data(
        file=path,
        content_prefix = "<FILE_CONTENT_START>",
        content_suffix = "<FILE_CONTENT_END>"
        )
    
    messages = [
        sm,
        um,
    ]
    
    tools = [
        current_datetime_function_tool,
        write_file_tool
    ]

    tool_registry = ToolRegistry()

    tool_registry.add_tools(tools)
    
    try:
        response = agent.get_response(
            messages=messages,
            settings=settings,
            tool_registry=tool_registry
        )
        logging.debug(response.response)
    except Exception as e:
        logging.exception(f"Error: {e}")

@timing_decorator
async def main(paths):
    # Local OpenAI-compatible API, like vllm or llama-cpp-server
    api = OpenAIChatAPI(
        api_key="",
        base_url="http://127.0.0.1:8000/v1",
        model="unsloth/gemma-4-E4B-it-GGUF:Q4_K_M",
        )
    
    settings = api.get_default_settings()

    # Set sampling settings
    settings.temperature = 0.25
    settings.top_p = 0.5

    # Create the ChatAPIAgent
    agent = ChatToolAgent(chat_api=api, log_to_file=True, log_output=False)
    
    semaphore = asyncio.Semaphore(4)
    
    async def bounded_task(path):
        async with semaphore:
            await asyncio.to_thread(task, agent, settings, path)

    tasks = [bounded_task(path) for path in paths]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Specify and create the ouput directory
    log_dir = Path.cwd() / "output"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Define the full path for the log file
    log_file = log_dir / "runtime.log"

    logging.basicConfig(filename=log_file, format='%(asctime)s - %(funcName)s: %(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        prog = 'Asynchoronous Code Review Agent',
        description = 'Using LLM, review source codes for security issues'
        )
    parser.add_argument("filename", nargs='*', help="filename(s) to review")
    parser.add_argument("-d", "--directory", help="directory for recursively reviewing all files")
    args = parser.parse_args()
    
    if not args.filename and not args.directory:
        parser.print_help()
        sys.exit()
        
    paths = []
    logging.debug(f"filename: {len(args.filename)}")
    logging.debug(f"directory: {args.directory}, {type(args.directory)} ")

    if args.filename:
        paths.extend([file for file in args.filename if Path(file).exists()])
    elif args.directory:
        paths.extend([child for child in sorted(Path(args.directory).rglob('*')) if child.suffix in {".sol", ".py", ".conf", ".c", ".cpp", ".js"}])
    
    if len(paths) == 0:
        print("Invalid filename or directory")
        sys.exit()

    asyncio.run(main(paths))