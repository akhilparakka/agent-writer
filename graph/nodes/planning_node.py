from langchain_core.language_models import LanguageModelLike
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from graph.nodes.base import BaseNode
from graph.state import WriterState
from typing import Dict, Any
from pathlib import Path


class PlanningNode(BaseNode):
    def __init__(
        self,
        llm: LanguageModelLike,
        prompt_template_path: Path = Path(__file__).parent / "prompts" / "plan.txt",
    ):
        self.llm = llm
        self.prompt_template = self._load_prompt_template(prompt_template_path)
        self.chain = self._create_graph()

    def _load_prompt_template(self, path: Path):
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to load prompt template: {str(e)}")

    def _create_graph(self) -> Runnable:
        prompt = ChatPromptTemplate.from_messages([("user", self.prompt_template)])
        return prompt | self.llm | StrOutputParser()

    def execute(self, state: WriterState) -> Dict[str, Any]:
        try:
            plan = self.chain.invoke({"instructions": state["initial_prompt"]})
            return {"plan": plan}
        except Exception as e:
            return {"plan": str(e)}
