import time
import datetime
import inspect
import logging
from pathlib import Path
from functools import wraps
from pydantic import BaseModel, Field
from ToolAgents import FunctionTool

def timing_decorator(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            logging.info(f"{args}: {end_time - start_time:.2f} seconds")
            return result
        return wrapper
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logging.info(f"{args}: {end_time - start_time:.2f} seconds")
            return result
        return wrapper

class WriteFileInput(BaseModel):
    """Input for writing to a file."""

    filename: str = Field(..., description="The name of the file to write to")
    content: str = Field(..., description="The content to write to the file")


def get_current_datetime(output_format: str):
    """
    Get the current date and time in the given format.

    Args:
         output_format: formatting string for the date and time
    """

    return datetime.datetime.now().strftime(output_format)


def write_file(input_data: WriteFileInput) -> str:
    """
    Write content to a file.
    Args:
        input_data: The input for the file write operation.
    Returns:
        A message indicating the result of the operation.
    """
    # Restrict file write to the output directory
    full_path = Path.cwd() / "output" / Path(input_data.filename).name
    try:
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w") as file:
            file.write(input_data.content)
        return f"Successfully wrote to file '{input_data.filename}'."
    except Exception as e:
        return f"Error writing to file: {str(e)}"

current_datetime_function_tool = FunctionTool(get_current_datetime)
current_datetime_function_tool.disable_confirmation()

write_file_tool = FunctionTool(write_file)
write_file_tool.disable_confirmation()