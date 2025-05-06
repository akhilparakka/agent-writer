from abc import ABC, abstractmethod
from langchain_core.language_models import LanguageModelLike
from graph.state import WriterState
from typing import Dict, Any


class BaseNode(ABC):
    def __init__(self, llm: LanguageModelLike):
        self.llm = llm

    @abstractmethod
    def execute(self, state: WriterState) -> Dict[str, Any]:
        pass

    def __call__(self, state: WriterState) -> Dict[str, Any]:
        return self.execute(state)
