


import json
from hashlib import sha256
from pathlib import Path
from typing import Optional

MEMORY_PATH = Path("memory.json")

def _hash(tool: str, args: dict) -> str:
    key_str = f"{tool}:{json.dumps(args, sort_keys=True)}"
    return sha256(key_str.encode()).hexdigest()

def load_memory() -> dict:
    if MEMORY_PATH.exists():
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory: dict):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def check_memory(tool: str, args: dict) -> Optional[dict]:
    memory = load_memory()
    key = _hash(tool, args)
    return memory.get(key)

def store_memory(tool: str, args: dict, result: dict):
    memory = load_memory()
    key = _hash(tool, args)
    memory[key] = result
    save_memory(memory)
