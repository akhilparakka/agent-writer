from langgraph.graph import MessagesState
from typing_extensions import TypedDict


class WriterState(TypedDict):
    initial_prompt: str
    plan: str
