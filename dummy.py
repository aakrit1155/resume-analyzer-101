import time
from typing import Any, List

from langchain_core.messages import AIMessage


class DummyLLM:
    def __init__(self, *args, **kwargs):
        print("DummyLLM initialized with args:", args)
        print("DummyLLM initialized with kwargs:", kwargs)

    def invoke(*args, **kwargs) -> AIMessage:
        time.sleep(5)
        return AIMessage(content="Test test test, this is a test message")
