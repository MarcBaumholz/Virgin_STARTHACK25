from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient, models
from data_loader import load_csv_as_documents
from config import QDRANT_URL, QDRANT_API_KEY
import time

def build_qdrant_vectorstore(csv_path: str, collection_name: str = "virgin_projects"):
    """
    Builds and returns a Qdrant vectorstore from the given CSV file
    """
    # Load texts and metadata using proper encoding
    try:
        texts, metadatas = load_csv_as_documents(csv_path)
    except UnicodeDecodeError:
        # If UTF-8 fails, try different encodings
        texts, metadatas = load_csv_as_documents(csv_path)
    
    # Initialize embedding model with explicit params
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )
    
    # Initialize Qdrant client with retry logic
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            client = QdrantClient(
                url=QDRANT_URL, 
                api_key=QDRANT_API_KEY,
                prefer_grpc=False,
                timeout=10
            )
            
            # Check if collection exists, if not create it
            collections = client.get_collections().collections
            collection_exists = any(col.name == collection_name for col in collections)
            
            if not collection_exists:
                # Create collection with proper configuration
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=384,  # Dimension for all-MiniLM-L6-v2
                        distance=models.Distance.COSINE
                    )
                )
            
            # Create vectorstore without force_recreate
            vectorstore = Qdrant(
                client=client,
                collection_name=collection_name,
                embeddings=embeddings
            )
            
            # Delete existing collection if it exists
            if collection_exists:
                client.delete_collection(collection_name=collection_name)
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=384,
                        distance=models.Distance.COSINE
                    )
                )
            
            # Add texts in batches
            if texts and metadatas:
                batch_size = 100
                for i in range(0, len(texts), batch_size):
                    batch_texts = texts[i:i + batch_size]
                    batch_metadata = metadatas[i:i + batch_size]
                    vectorstore.add_texts(texts=batch_texts, metadatas=batch_metadata)
            
            return vectorstore
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed to connect to Qdrant after {max_retries} attempts: {str(e)}")
            print(f"Connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2

if __name__ == "__main__":
    csv_path = "Virgin_StartHack_Sample_Initiatives.csv"
    store = build_qdrant_vectorstore(csv_path)
    print("Vectorstore in Qdrant wurde erstellt.")