


from pathlib import Path
import datetime

def load_prompt(path: str) -> str:
    """
    Loads a text prompt file from disk.

    Args:
        path (str): The relative path to the prompt file.

    Returns:
        str: The contents of the file as a stripped string.
    """
    return Path(path).read_text(encoding="utf-8").strip()

def log(source: str, message: str) -> None:
    """
    Logs a message with a timestamp and source label.

    Args:
        source (str): A short label for the message source (e.g., 'executor', 'planner').
        message (str): The message to print to the console.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{source}] {message}")
