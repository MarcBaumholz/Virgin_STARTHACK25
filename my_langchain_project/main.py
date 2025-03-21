from agent import create_advanced_qa_agent
from vector_store import build_qdrant_vectorstore

def main():
    csv_path = "Virgin_StartHack_Sample_Initiatives.csv"
    vectorstore = build_qdrant_vectorstore(csv_path)
    
    # Create the advanced agent with multiple tools
    agent = create_advanced_qa_agent(vectorstore, csv_path)
    
    print("Ask questions about Virgin initiatives (Type 'exit' to end):")
    while True:
        user_query = input(">> ")
        if user_query.lower() == "exit":
            break
            
        try:
            result = agent.run(user_query)
            print("\nAgent Response:")
            print(result)
            print("\n---\n")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()