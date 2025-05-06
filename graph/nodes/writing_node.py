from graph.nodes.base import BaseNode
from graph.state import WriterState
from typing import Dict, Any


class WritingNode(BaseNode):
    def execute(self, state: WriterState) -> Dict[str, Any]:
        # messages = [{"content": f"Write based on {state.plan}"}]
        # response = self.llm.invoke(messages)
        return {"content": "I am the content"}
