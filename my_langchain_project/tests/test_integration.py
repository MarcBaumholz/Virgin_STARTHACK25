import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from vector_store import build_qdrant_vectorstore
from agent import create_advanced_qa_agent, OpenRouterLLM
import pandas as pd

@pytest.fixture(scope="module")
def test_data():
    return {
        "csv_path": "Virgin_StartHack_Sample_Initiatives.csv",
        "test_queries": [
            "How many digital initiatives are there?",
            "What are the main sustainability projects?",
            "List all Virgin companies"
        ]
    }

@pytest.fixture(scope="module")
def vectorstore(test_data):
    return build_qdrant_vectorstore(test_data["csv_path"])

@pytest.fixture(scope="module")
def qa_agent(vectorstore, test_data):
    return create_advanced_qa_agent(vectorstore, test_data["csv_path"])

def test_llm_basic_response():
    llm = OpenRouterLLM()
    prompt = "What is Virgin Group?"
    response = llm.predict(prompt)
    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\nLLM Response to '{prompt}':\n{response}")

def test_vectorstore_search(vectorstore):
    results = vectorstore.similarity_search("digital initiatives", k=2)
    assert len(results) == 2
    print("\nVector Search Results:")
    for doc in results:
        print(f"- {doc.page_content[:200]}...")

def test_qa_chain(qa_agent, test_data):
    print("\nTesting QA Chain with multiple queries:")
    for query in test_data["test_queries"]:
        response = qa_agent.run(query)
        assert isinstance(response, str)
        assert len(response) > 0
        print(f"\nQuery: {query}")
        print(f"Response: {response}\n---")

def test_data_loading(test_data):
    df = pd.read_csv(test_data["csv_path"])
    print(f"\nDataset Statistics:")
    print(f"Total Initiatives: {len(df)}")
    print(f"Companies: {', '.join(df['Virgin Company'].unique())}")
    assert len(df) > 0
