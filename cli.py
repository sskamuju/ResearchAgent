


import os
from dotenv import load_dotenv

load_dotenv()

name = os.getenv("USER_NAME", "Agent")
print(f"Hello from Docker, {name}!")
