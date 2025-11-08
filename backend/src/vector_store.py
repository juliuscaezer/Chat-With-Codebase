import os 
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    EMBEDDING_MODEL_NAME
)

from src.data_loader import load_git_repo
from src.text_processing import split_code_documents
# Test mode - to process only a few vectors to see if the code is successful 
TEST_MODE = True 


EMBEDDING_DIMENSION = 768

def create_vector_store():
    """
    Creates and persists a vector store in Pinecone.
    This is the "Ingestion" step.
    """
    print("Starting vector store creation...")
    
    # 1. Initialize Pinecone client
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # 2. Check if the index already exists.
    if PINECONE_INDEX_NAME in [index['name'] for index in pc.list_indexes()]:
        print(f"Index '{PINECONE_INDEX_NAME}' already exists. Deleting...")
        # Delete the index to start fresh
        pc.delete_index(PINECONE_INDEX_NAME)
        # Wait a moment for the deletion to register
        time.sleep(5) 
        print("Old index deleted.")

    # 3. Create a new index
    # We specify the dimension (768) and the "metric" (cosine similarity)
    print(f"Creating new index: {PINECONE_INDEX_NAME}...")
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    # Wait for the index to be ready
    while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
        print("Waiting for index to be ready...")
        time.sleep(5)
    print("Index created successfully.")

    # 4. Load the documents (fast, from local cache)
    documents = load_git_repo()
    if not documents:
        print("No documents loaded, stopping.")
        return

    # 5. Split the documents
    chunks = split_code_documents(documents)
    if not chunks:
        print("No chunks created, stopping.")
        return

    # 6. Apply Test Mode slice
    if TEST_MODE:
        print(f"\n*** TEST MODE: Slicing chunks from {len(chunks)} to 100. ***\n")
        chunks = chunks[:500]

    # 7. Initialize the embedding model (same as before)
    model_kwargs = {'trust_remote_code': True}
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs
    )
    
    print(f"Embedding {len(chunks)} chunks and uploading to Pinecone...")
    
    # 8. Upload the documents to Pinecone
    # LangChain's 'from_documents' handles all the batching for us.
    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME
    )
    
    print(f"Vector store created and populated successfully in Pinecone.")

def get_retriever():
    """
    Loads the existing Pinecone vector store and returns a retriever object.
    This is the "Retrieval" step for the API.
    """
    
    # 1. Initialize the embedding model
    model_kwargs = {'trust_remote_code': True}
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs
    )
    
    # 2. Connect to the existing Pinecone index
    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )
    
    # 3. Create and return a retriever
    return vector_store.as_retriever(search_kwargs={"k": 5})

# --- Test Block ---
if __name__ == "__main__":
    """
    If you run this file directly (e.g., 'python -m src.vector_store'),
    it will execute the full ingestion process into Pinecone.
    """
    create_vector_store()