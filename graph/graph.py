from langgraph.graph.state import CompiledStateGraph
from graph.nodes.planning_node import planning_node
from graph.nodes.writing_node import writing_node
from graph.nodes.saving_node import saving_node
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from graph.state import WriterState
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()


class Writer:
    def __init__(self, tools: BaseTool):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o"
        ).bind_tools(tools)
        self._graph: Optional[CompiledStateGraph] = None

    def create_writer(self) -> CompiledStateGraph:
        graph_builder = StateGraph(WriterState)
        graph_builder.add_node("planning_node", planning_node)
        graph_builder.add_node("writing_node", writing_node)
        graph_builder.add_node("saving_node", saving_node)
        graph_builder.set_entry_point("planning_node")
        graph_builder.add_edge("planning_node", "writing_node")
        graph_builder.add_edge("writing_node", "saving_node")
        return graph_builder.compile()


tools = []
writer = Writer(tools=tools)
graph = writer.create_writer()
