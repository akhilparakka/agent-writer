from langgraph.graph.state import CompiledStateGraph
from graph.nodes.planning_node import PlanningNode
from graph.nodes.writing_node import WritingNode
from graph.nodes.saving_node import SavingNode
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from graph.state import WriterState
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()


class Writer:
    def __init__(
        self,
        tools: list = None,
        model: str = "gpt-4o",
        prompt_template_path: Path = Path(
            "graph/nodes/prompts/plan.txt"
        ),  # Default path
    ):
        self.llm = self._init_llm(model, tools or [])
        self.prompt_template_path = prompt_template_path
        self._graph = None

    def _init_llm(self, model: str, tools: list) -> ChatOpenAI:
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=model,
            temperature=0.7,
        ).bind_tools(tools)

    @property
    def graph(self) -> CompiledStateGraph:
        """Lazy-loaded compiled graph"""
        if not self._graph:
            self._graph = self._build_graph()
        return self._graph

    def _build_graph(self) -> CompiledStateGraph:
        """Construct and compile the workflow graph"""
        graph_builder = StateGraph(WriterState)

        nodes = {
            "planning": PlanningNode(
                llm=self.llm, prompt_template_path=self.prompt_template_path
            ),
            "writing": WritingNode(llm=self.llm),
            "saving": SavingNode(llm=self.llm),
        }

        for name, node in nodes.items():
            graph_builder.add_node(name, node.execute)

        graph_builder.set_entry_point("planning")
        graph_builder.add_edge("planning", "writing")
        graph_builder.add_edge("writing", "saving")

        return graph_builder.compile()


writer = Writer()
graph = writer.graph
