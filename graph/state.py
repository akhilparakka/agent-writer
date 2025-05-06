from typing import TypedDict, Optional, List


class WriterState(TypedDict):
    initial_prompt: str
    plan: str
    final_doc: Optional[str]
    num_steps: int
    errors: Optional[List[str]]
    word_count: int
