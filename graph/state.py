# from langgraph.graph import StateGraph
# from langchain_core.language_models import LanguageModelLike
# from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict


class WriterState(TypedDict):
    initial_prompt: str
    plan: str


# def create_graph(llm: LanguageModelLike) -> CompiledStateGraph:
#     graph = StateGraph(WriterState)

#     graph.add_node("planning_node", planning_node)
#     graph.add_node("writing_node", writing_node)
#     graph.add_node("saving_node", saving_node)

#     return graph.compile()
