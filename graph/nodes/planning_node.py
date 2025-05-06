from langchain_core.language_models import LanguageModelLike
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from graph.state import WriterState
from graph.nodes.base import BaseNode
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class PlanningNode(BaseNode):
    def __init__(
        self,
        llm: LanguageModelLike,
        prompt_template_path: Path = Path(__file__).parent / "prompts" / "plan.txt",
    ):
        super().__init__(llm)
        self.prompt_template = self._load_prompt_template(prompt_template_path)
        self.chain = self._create_chain()

    def _load_prompt_template(self, path: Path) -> str:
        try:
            if not path.exists():
                raise FileNotFoundError(f"Prompt file not found at {path}")
            return path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Prompt template loading failed: {str(e)}")
            raise

    def _create_chain(self) -> Runnable:
        prompt = ChatPromptTemplate.from_messages([("user", self.prompt_template)])
        return prompt | self.llm | StrOutputParser()

    def execute(self, state: WriterState) -> Dict[str, Any]:
        try:
            plan = self.chain.invoke({"instructions": state["initial_prompt"]})
            return {"plan": plan}
        except Exception as e:
            logger.error(f"Planning failed: {str(e)}")
            return {"plan": str(e), "error": True}
