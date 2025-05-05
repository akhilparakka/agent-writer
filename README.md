# LangGraph Writing Assistant

## Overview
This project implements a writing assistant using LangGraph, a framework for building stateful, graph-based applications. The assistant leverages OpenAI's GPT-4o model to plan, write, and save content, orchestrated through a state graph.

## Features
- **Planning:** Generates a plan for the writing task
- **Writing:** Produces content based on the plan using ChatOpenAI
- **Saving:** Stores the output (implementation details in saving_node.py)
- **Configurable:** Via a langgraph.json file for LangGraph Studio integration

## Project Structure
```
writer/
├── graph/
│   ├── graph.py
│   ├── state.py
│   ├── nodes/
│   │   ├── planning_node.py
│   │   ├── writing_node.py
│   │   ├── saving_node.py
│   ├── langgraph.json
├── .env
├── pyproject.toml
├── requirements.txt
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
conda create -n luma-agent python=3.11
conda activate luma-agent
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
This starts an in-memory server at [http://127.0.0.1:2024](http://127.0.0.1:2024).

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
