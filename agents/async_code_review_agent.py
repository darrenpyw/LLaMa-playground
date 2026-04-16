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

    um = ChatMessage.create_user_message(f"""
    Analyze the attached file {path} for security misconfigurations.
    The file content is delimited between <FILE_CONTENT_START> and <FILE_CONTENT_END>.
    First, retrieve the current time in the format: %Y-%m-%d_%H-%M.
    Then write the analysis to a file named '<retrieved_timestamp>-<file_analyzed>.md' (replace <retrieved_timestamp> with the actual timestamp, replace <file_analyzed> with the actual filename).
    
    Strictly use the example template below for markdown output:
    **File Analyzed:** `../damn-vulnerable-defi/src/abi-smuggling/AuthorizedExecutor.sol`
    **Analysis Timestamp:** 2026-04-13_16-54
    ## Findings

    ### 1. Abstraction/Access Control Flaw in `execute` function [Impact - HIGH]

    The `execute` function relies on a mapping `permissions` to authorize arbitrary function calls. 
    
    **Vulnerability Context:**
    The core security relies on `permissions[getActionId(selector, msg.sender, target)]` correctly checking if the current caller is authorized to execute the specified action on the target.

    **Potential Issue (Abuse via `getActionId`):**
    The `getActionId` function computes the permission key as:
    `keccak256(abi.encodePacked(selector, executor, target))`

    **Proof of Concept Exploit Code:**
    ```
    Vulnerability exploit code
    ```

    **Recommendation:**
    1. **Input Validation:** Ensure that the `selector` extracted from `actionData` is a valid function selector for a known interface or contract, preventing the execution of arbitrary, unintended code if the logic for deriving the permission key is flawed.
    2. **Permission Granularity Review:** Thoroughly audit the `permissions` mapping to ensure that permissions are correctly set during `setPermissions` and that no unintended combinations grant access.

    """)
    
    um.add_text_file_data(file=path,
                          content_prefix = "<FILE_CONTENT_START>",
                          content_suffix = "<FILE_CONTENT_END>")
    
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
    settings.temperature = 1.0
    settings.top_p = 1.0

    # Create the ChatAPIAgent
    agent = ChatToolAgent(chat_api=api, log_to_file=False, log_output=False)
    
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
    
    if len(args.filename) == 0 and args.directory is None:
        parser.print_help()
        sys.exit()
        
    paths = []
    logging.debug(f"filename: {len(args.filename)}")
    logging.debug(f"directory: {args.directory}, {type(args.directory)} ")

    if args.filename:
        paths.extend([file for file in args.filename if Path(file).exists()])
    elif args.directory is not None:
        paths.extend([child for child in sorted(Path(args.directory).rglob('*')) if child.suffix in {".sol", ".py", ".conf", ".c", ".cpp", ".js", ".json"}])
    
    if len(paths) == 0:
        print("Invalid filename or directory")
        sys.exit()

    asyncio.run(main(paths))