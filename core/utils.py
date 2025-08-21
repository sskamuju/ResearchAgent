


from pathlib import Path
import datetime

def load_prompt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip()

def log(source: str, message: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{source}] {message}")
