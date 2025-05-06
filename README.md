# TextWeaver

## Overview

This project implements a writing assistant using LangGraph, a framework for building stateful, graph-based applications. The assistant leverages OpenAI's GPT-4 model to plan, write, and save content, orchestrated through a state graph. The prompt engineering and workflow design are inspired by the research paper ["LONGWRITER: UNLEASHING 10,000+ WORD GENERATION FROM LONG CONTEXT LLMS"](https://arxiv.org/pdf/2408.07055).

> **Note on LLM Token Handling**: Large Language Models (LLMs) typically have an asymmetric relationship with tokens - they can process (take in) more tokens than they can generate (output) in a single response. This limitation is by design and helps maintain quality and coherence in the outputs while allowing for comprehensive context understanding.

## Features

- **Planning:** Generates a plan for the writing task using prompting strategies from research
- **Writing:** Produces content based on the plan using ChatOpenAI
- **Saving:** Stores the output (implementation details in saving_node.py)
- **Configurable:** Via a langgraph.json file for LangGraph Studio integration

## Project Structure

```
writer/
├── graph/
│   ├── graph.py        # Main graph definition
│   ├── state.py        # State management
│   ├── nodes/          # Graph node implementations
│   │   ├── __init__.py
│   │   ├── planning_node.py
│   │   ├── writing_node.py
│   │   ├── saving_node.py
│   ├── utils/          # Utility functions
│   │   ├── utils.py
│   ├── langgraph.json  # LangGraph configuration
├── tests/              # Unit tests
│   ├── __init__.py
│   ├── test_nodes/
├── .env                # Environment variables
├── pyproject.toml      # Project metadata and dependencies
├── requirements.txt    # Direct dependencies
├── README.md
├── .gitignore
```

## Prerequisites

- Python 3.11
- Conda (for environment management)
- OpenAI API key (for ChatOpenAI)

## Setup

### Clone the repository:

```bash
git clone <repository-url>
cd writer
```

### Create a Conda environment:

```bash
conda create -n writer-agent python=3.11
conda activate writer-agent
```

### Install dependencies:

```bash
python -m pip install -e .
```

### Set up environment variables:

Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your-api-key" > .env
```

Replace `your-api-key` with your OpenAI API key.

## Usage

### Run the LangGraph development server:

```bash
cd graph/
langgraph dev
```

This starts an in-memory server at [https://smith.langchain.com/studio/thread?baseUrl=http%3A%2F%2F127.0.0.1%3A2024&mode=graph](https://smith.langchain.com/studio/thread?baseUrl=http%3A%2F%2F127.0.0.1%3A2024&mode=graph).

### Access LangGraph Studio:

Open LangGraph Studio in your browser (requires a LangSmith account).

### Interact with the graph:

Use the Studio UI to visualize and run the graph, or interact via the API ([http://127.0.0.1:2024/docs](http://127.0.0.1:2024/docs)).

## Development

- **Modify the graph:** Edit graph.py to adjust nodes or edges
- **Add nodes:** Implement new nodes in graph/nodes/
- **Test locally:** Use `langgraph dev` for rapid iteration

## Dependencies

- langgraph
- langchain-core
- langchain-openai
- python-dotenv

See `pyproject.toml` for the full list.

## References

- [LONGWRITER: UNLEASHING 10,000+ WORD GENERATION FROM LONG CONTEXT LLMS](https://arxiv.org/pdf/2408.07055) - Research paper that inspired the prompting strategies used in this project.
