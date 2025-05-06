from graph.nodes.base import BaseNode
from graph.state import WriterState
from typing import Dict, Any


class SavingNode(BaseNode):
    def execute(self, state: WriterState) -> Dict[str, Any]:
        # # Implementation that might use different LLM parameters
        # messages = [{"content": f"Save {state.content}"}]
        # response = self.llm.invoke(messages)
        return {"saved_content": "I am the saviour"}
