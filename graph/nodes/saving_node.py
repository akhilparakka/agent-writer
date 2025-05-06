from langchain_core.language_models import LanguageModelLike
from pathlib import Path
from typing import Dict, Any
from graph.nodes.base import BaseNode
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SavingNode(BaseNode):
    def __init__(
        self,
        llm: LanguageModelLike,
        output_dir: Path = Path("outputs"),
        timestamp_format: str = "%Y%m%d_%H%M%S",
    ):
        """
        Initialize the saving node (no LLM required).

        Args:
            output_dir: Directory to save documents (default: ./outputs)
            timestamp_format: Format for filename timestamps (default: YYYYMMDD_HHMMSS)
        """
        super().__init__(llm)
        self.output_dir = output_dir
        self.timestamp_format = timestamp_format
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, base_name: str, llm_name: str) -> str:
        """Generate standardized filename with timestamp."""
        timestamp = datetime.now().strftime(self.timestamp_format)
        return f"{base_name}_{llm_name}_{timestamp}.md"

    def _save_to_disk(self, content: str, filename: str) -> Path:
        """Save content to disk with error handling."""
        try:
            filepath = self.output_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Saved file: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save {filename}: {str(e)}")
            raise

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        enhanced_doc = (
            f"# Generated Document\n\n"
            f"**Prompt**: {state.get('initial_prompt', 'N/A')}\n\n"
            f"{state['final_doc']}\n\n"
            f"---\n"
            f"**Word count**: {state['word_count']}\n"
        )

        doc_filename = self._generate_filename("document", "gpt-4o")
        doc_path = self._save_to_disk(enhanced_doc, doc_filename)

        return {
            "num_steps": state.get("num_steps", 0) + 1,
        }
