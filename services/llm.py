from langchain_openai import ChatOpenAI
from config.llm_conf import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, REQUEST_TIMEOUT

def build_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=LLM_MODEL,
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,     # https://api.deepseek.com 即可，SDK 自动拼路径
        temperature=0,
        timeout=REQUEST_TIMEOUT,
        max_retries=2,
        streaming=True,
    )