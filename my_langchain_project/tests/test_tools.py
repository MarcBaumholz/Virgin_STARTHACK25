import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from agent import create_virgin_tools
from vector_store import build_qdrant_vectorstore

@pytest.fixture
def setup_tools():
    csv_path = "Virgin_StartHack_Sample_Initiatives.csv"
    vectorstore = build_qdrant_vectorstore(csv_path)
    tools = create_virgin_tools(vectorstore, csv_path)
    return tools

def test_count_projects_tool(setup_tools):
    count_tool = next(tool for tool in setup_tools if tool.name == "Count_Projects")
    result = count_tool.func("digital")
    assert isinstance(result, str)
    assert "projects matching" in result

def test_get_companies_tool(setup_tools):
    companies_tool = next(tool for tool in setup_tools if tool.name == "Get_Companies")
    result = companies_tool.func("")
    assert isinstance(result, str)
    assert "Companies:" in result

def test_summarize_tool(setup_tools):
    summarize_tool = next(tool for tool in setup_tools if tool.name == "Summarize_Projects")
    result = summarize_tool.func()
    assert isinstance(result, str)
    assert len(result) > 0
