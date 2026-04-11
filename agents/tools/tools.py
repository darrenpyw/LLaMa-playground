import time
import datetime
from pydantic import BaseModel, Field
from ToolAgents import FunctionTool

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\nTask runtime: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def get_current_datetime(output_format: str):
    """
    Get the current date and time in the given format.

    Args:
         output_format: formatting string for the date and time
    """

    return datetime.datetime.now().strftime(output_format)


current_datetime_function_tool = FunctionTool(get_current_datetime)