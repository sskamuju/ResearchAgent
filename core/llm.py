


import os
from openai import OpenAI
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai


load_dotenv()
client = wrap_openai(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))