from agent import OpenRouterLLM
import pandas as pd

def extract_companies(csv_path: str) -> str:
    """Extract and analyze companies from initiatives"""
    df = pd.read_csv(csv_path)
    llm = OpenRouterLLM()
    companies = df['Virgin Company'].unique()
    prompt = f"""Analyze these Virgin companies and their initiatives:
    Companies: {', '.join(companies)}
    
    Provide a brief analysis of each company's focus areas and strengths."""
    
    return llm.predict(prompt)

def extract_challenges(csv_path: str) -> str:
    """Extract challenges from initiatives"""
    llm = OpenRouterLLM()
    prompt = (
        "Based on the Virgin initiatives data, extract and summarize "
        "the key challenges being addressed across all projects."
    )
    return llm.predict(prompt)

def rate_initiatives(csv_path: str) -> dict:
    """Rate initiatives on multiple dimensions"""
    llm = OpenRouterLLM()
    df = pd.read_csv(csv_path)
    
    ratings = {
        'sustainability': llm.predict("Rate each initiative's sustainability impact (1-10)"),
        'innovation': llm.predict("Rate each initiative's innovation level (1-10)"),
        'feasibility': llm.predict("Rate each initiative's implementation feasibility (1-10)")
    }
    
    return ratings
