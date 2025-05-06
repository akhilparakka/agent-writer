from langchain_core.language_models import LanguageModelLike
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from graph.nodes.base import BaseNode
from graph.state import WriterState
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class WritingNode(BaseNode):
    def __init__(
        self,
        llm: LanguageModelLike,
        prompt_template_path: Path = Path(__file__).parent / "prompts" / "write.txt",
        max_steps: int = 50,
        max_context_length: int = 4000,
    ):
        """
        Initialize the writing node.

        Args:
            llm: Language model instance
            prompt_template_path: Path to the writing prompt template
            max_steps: Maximum allowed planning steps
            max_context_length: Maximum characters of previous text to include in context
        """
        super().__init__(llm)
        self.max_steps = max_steps
        self.max_context_length = max_context_length
        self.prompt_template = self._load_prompt_template(prompt_template_path)
        self.chain = self._create_chain()

    def _load_prompt_template(self, path: Path) -> str:
        """Load and validate the writing prompt template."""
        try:
            if not path.exists():
                raise FileNotFoundError(f"Prompt file not found at {path}")

            return path.read_text(encoding="utf-8")

        except Exception as e:
            logger.error(f"Prompt template loading failed: {str(e)}")
            raise RuntimeError(f"Could not initialize writing node: {str(e)}") from e

    def _create_chain(self) -> Runnable:
        """Create the LangChain runnable pipeline."""
        prompt = ChatPromptTemplate.from_messages([("user", self.prompt_template)])
        return prompt | self.llm | StrOutputParser()

    def _count_words(self, text: str) -> int:
        """Count words in text (helper method)."""
        return len(text.split())

    def _process_step(self, step: str, instruction: str, current_text: str) -> str:
        """
        Process a single writing step.

        Args:
            step: Current step/heading from the plan
            instruction: Original user instruction
            current_text: All generated text so far

        Returns:
            Generated content for this step
        """
        try:
            if not step.strip():
                logger.warning("Empty step encountered")
                return ""

            context = current_text[-self.max_context_length :] if current_text else ""

            result = self.chain.invoke(
                {
                    "instructions": instruction,
                    "plan": step,
                    "text": context,
                    "STEP": step,
                }
            )

            return result

        except Exception as e:
            logger.error(f"Failed to process step '{step[:50]}...': {str(e)}")
            return f"[SECTION GENERATION FAILED: {step[:100]}]"

    def count_words(self, text: str):
        """
        Count the number of words in the given text.

        Args:
            text (str): The input text to count words from.

        Returns:
            int: The number of words in the text.
        """
        words = text.split()
        return len(words)

    def execute(self, state: WriterState) -> Dict[str, Any]:
        """
        Execute the writing process based on the plan.

        Args:
            state: Current workflow state containing:
                - initial_prompt: Original user instruction
                - plan: Generated writing plan
                - num_steps: Optional step counter

        Returns:
            Dictionary with:
                - final_doc: Generated document
                - word_count: Total word count
                - steps_processed: Number of successfully processed steps
                - errors: List of errors (if any)
                - num_steps: Updated step counter
        """
        try:
            if not state.get("initial_prompt"):
                raise ValueError("Missing initial_prompt in state")
            if not state.get("plan"):
                raise ValueError("No writing plan provided in state")

            instruction = state["initial_prompt"]
            plan = state["plan"].strip().replace("\n\n", "\n")
            steps = [s.strip() for s in plan.split("\n") if s.strip()]
            num_steps = state.get("num_steps", 0) + 1

            if len(steps) > self.max_steps:
                error_msg = (
                    f"Plan exceeds maximum steps ({len(steps)} > {self.max_steps})"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            results = []
            current_text = ""
            errors = []

            for step in steps:
                try:
                    result = self._process_step(step, instruction, current_text)
                    results.append(result)
                    current_text += f"{result}\n\n"
                except Exception as e:
                    errors.append(f"Step '{step[:50]}...': {str(e)}")
                    logger.error(f"Error processing step: {str(e)}")
                    continue

            final_doc = "\n\n".join(results)

            return {
                "final_doc": final_doc,
                "word_count": self.count_words(final_doc),
                "steps_processed": len(results),
                "errors": errors if errors else None,
                "num_steps": num_steps,
            }

        except Exception as e:
            logger.critical(f"Writing node execution failed: {str(e)}", exc_info=True)
            return {
                "final_doc": f"DOCUMENT GENERATION FAILED: {str(e)}",
                "word_count": 0,
                "steps_processed": 0,
                "error": str(e),
                "num_steps": state.get("num_steps", 0),
            }
