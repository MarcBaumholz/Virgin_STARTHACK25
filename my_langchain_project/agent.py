import os
import json
import requests
import pandas as pd
from langchain_core.language_models.llms import LLM
from langchain.chains import RetrievalQA, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_experimental.tools import PythonREPLTool
from typing import List, Dict, Optional, ClassVar
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from langchain_community.vectorstores import Qdrant
from typing_extensions import Annotated
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from config import OPENROUTER_API_KEY, QDRANT_URL, QDRANT_API_KEY
from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.agent import AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
import re
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.format_scratchpad import format_log_to_str
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# -------------------------------
# Custom LLM über OpenRouter, der ein kostenloses Google-Modell anspricht.
# -------------------------------
class OpenRouterLLM(LLM):
    """
    Ein einfacher LLM-Wrapper, der die OpenRouter-API nutzt.
    """
    model_name: str = "qwen/qwq-32b:free"  # Using Palm 2 as it's available on OpenRouter
    
    @property
    def _llm_type(self) -> str:
        return "openrouter"

    def _call(self, prompt: str, stop=None) -> str:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:8000",  # Required for OpenRouter
            "X-Title": "LangChain QA Agent",  # Optional, but good practice
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant that answers questions about Virgin initiatives based on the provided context. Answer in the same language as the question."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API Error: {str(e)}\nResponse: {response.text if hasattr(response, 'text') else 'No response'}")

    def predict(self, prompt: str, **kwargs) -> str:
        return self._call(prompt, **kwargs)

# -------------------------------
# Aufbau des RetrievalQA-Agenten mit LangChain
# -------------------------------
def create_retrieval_qa_chain(vectorstore: Qdrant) -> RetrievalQA:
    """
    Erstellt eine RetrievalQA-Kette, die den Qdrant-Vektorstore als Retriever nutzt
    und den OpenRouterLLM als Sprachmodell einbindet.
    """
    # Setze Callback Manager für Streaming (optional)
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    
    # Erstelle den benutzerdefinierten LLM
    llm = OpenRouterLLM()

    # Erstelle den RetrievalQA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        callback_manager=callback_manager,
        return_source_documents=True
    )
    return qa_chain

class CountProjectsArgsSchema(BaseModel):
    criteria: str

def create_virgin_tools(vectorstore, csv_path: str) -> List[Tool]:
    """Create tools for analyzing Virgin initiatives"""
    def read_data():
        return pd.read_csv(csv_path)

    def count_projects(criteria: str) -> str:
        df = read_data()
        count = df[df.apply(lambda row: any(str(criteria).lower() in str(val).lower() for val in row), axis=1)].shape[0]
        return f"There are {count} projects matching the criteria: {criteria}"

    def summarize_projects() -> str:
        llm = OpenRouterLLM()
        prompt = (
            "Analyze the following Virgin initiatives and summarize the key trends, "
            "core information, challenges, and successes."
        )
        return llm.predict(prompt)

    def assign_labels() -> str:
        llm = OpenRouterLLM()
        prompt = (
            "Analyze the Virgin initiatives and automatically assign labels that reflect "
            "the thematic focus (e.g., digital inclusion, sustainable aviation) and "
            "challenges of each company."
        )
        return llm.predict(prompt)

    def find_related() -> str:
        llm = OpenRouterLLM()
        prompt = (
            "Analyze the Virgin initiatives and group related projects that are "
            "thematically similar or have similar objectives. Describe the relationships."
        )
        return llm.predict(prompt)

    return [
        Tool(
            name="Search_Database",
            func=vectorstore.similarity_search,
            description="Search for relevant Virgin initiatives in the database"
        ),
        Tool(
            name="Data_Analysis",
            func=PythonREPLTool().run,
            description="Execute Python code for data analysis. Use pandas as pd to analyze the CSV data."
        ),
        Tool(
            name="Get_Initiative_Count",
            func=lambda x: f"Total initiatives: {len(read_data())}",
            description="Get the total number of initiatives"
        ),
        Tool(
            name="Get_Companies",
            func=lambda x: f"Companies: {', '.join(read_data()['Virgin Company'].unique())}",
            description="List all Virgin companies"
        ),
        StructuredTool.from_function(
            func=count_projects,
            name="Count_Projects",
            description="Counts projects matching given criteria",
            args_schema=CountProjectsArgsSchema
        ),
        Tool(
            name="Summarize_Projects",
            func=summarize_projects,
            description="Generate a summary of all Virgin initiatives"
        ),
        Tool(
            name="Assign_Labels",
            func=assign_labels,
            description="Automatically assign thematic labels to projects"
        ),
        Tool(
            name="Find_Related",
            func=find_related,
            description="Group and find relationships between projects"
        )
    ]

class VirginInitiativesPrompt:
    """Prompt template for Virgin initiatives analysis"""
    
    @staticmethod
    def create_prompt() -> PromptTemplate:
        template = """You are an AI analyzing Virgin initiatives. Use the following tools to help answer the question:
{tools}

Available tools include:
- Search and retrieve relevant initiatives
- Count projects matching criteria
- Generate summaries
- Assign thematic labels
- Find related projects
- Perform data analysis

Use the following format:
Question: the input question
Thought: consider what tools to use
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Question: {input}
{agent_scratchpad}"""

        return PromptTemplate(
            template=template,
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
        )

class VirginAgentOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> AgentAction | AgentFinish:
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        
        match = re.match(r"Action: (.*?)[\n]*Action Input: (.*)", llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: {llm_output}")
        
        action = match.group(1).strip()
        action_input = match.group(2).strip()
        
        return AgentAction(tool=action, tool_input=action_input, log=llm_output)

def create_advanced_qa_agent(vectorstore, csv_path: str) -> AgentExecutor:
    """Creates an advanced agent with multiple tools and memory"""
    llm = OpenRouterLLM()
    tools = create_virgin_tools(vectorstore, csv_path)
    
    # Create memory with updated configuration
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )
    
    # Create prompt template
    prompt = VirginInitiativesPrompt.create_prompt()
    
    # Create output parser
    output_parser = VirginAgentOutputParser()
    
    # Create agent chain using correct runnable sequence
    agent_chain = (
        prompt
        | RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"])
        )
        | llm
        | output_parser
    )
    
    # Create agent executor
    return AgentExecutor.from_agent_and_tools(
        agent=agent_chain,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

def analyze_trends(csv_path: str) -> str:
    """Analyze trends in Virgin initiatives"""
    df = pd.read_csv(csv_path)
    companies = df['Virgin Company'].value_counts()
    initiatives = len(df)
    
    trend_analysis = (
        f"Analysis of {initiatives} initiatives:\n"
        f"- Number of companies involved: {len(companies)}\n"
        f"- Most active companies: {', '.join(companies.head(3).index)}\n"
        f"- Key focus areas identified in initiatives"
    )
    return trend_analysis

def suggest_collaborations(csv_path: str) -> str:
    """Suggest potential collaborations between initiatives"""
    df = pd.read_csv(csv_path)
    # Simple collaboration suggestion based on company activities
    companies = df['Virgin Company'].unique()
    suggestions = [
        f"Potential collaboration between {companies[i]} and {companies[i+1]}"
        for i in range(len(companies)-1)
    ]
    return "\n".join(suggestions)

if __name__ == "__main__":
    # Beispiel: Verbindung zu Qdrant herstellen und den Agenten testen.
    from vector_store import build_qdrant_vectorstore
    csv_path = "Virgin_StartHack_Sample_Initiatives.csv"
    vectorstore = build_qdrant_vectorstore(csv_path)
    
    qa_chain = create_retrieval_qa_chain(vectorstore)
    query = "Welche Projekte fokussieren sich auf digitale Inklusion?"
    result = qa_chain({"query": query})
    print("Agent-Antwort:")
    print(result["result"])