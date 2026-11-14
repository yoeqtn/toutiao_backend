import os
from dotenv import load_dotenv
load_dotenv()
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-flash")

MAX_STEPS = 6          # agent 最多循环几次
REQUEST_TIMEOUT = 30   # 秒
