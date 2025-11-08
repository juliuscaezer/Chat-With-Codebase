import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Import our config and processing modules
from src.config import VECTOR_DB_PATH, EMBEDDING_MODEL_NAME
from src.data_loader import load_git_repo
from src.text_processing import split_code_documents

# --- THIS IS THE NEW LINE ---
# Set to True to only process 100 chunks, False to process all
# Disable this while deploying
TEST_MODE = True
# ----------------------------

def create_vector_store():
    """
    Creates and persists a vector store from the documents.
    This is the "Ingestion" step.
    """
    print("Starting vector store creation...")
    
    # 1. Check if the DB already exists
    if os.path.exists(VECTOR_DB_PATH):
        print(f"Deleting existing vector store at {VECTOR_DB_PATH}")
        shutil.rmtree(VECTOR_DB_PATH)
    
    # 2. Load the documents
    documents = load_git_repo()
    if not documents:
        print("No documents loaded, stopping.")
        return

    # 3. Split the documents
    chunks = split_code_documents(documents)
    if not chunks:
        print("No chunks created, stopping.")
        return

    # --- NEW: TEST MODE LOGIC ---
    if TEST_MODE:
        print(f"\n*** TEST MODE: Slicing chunks from {len(chunks)} to 100. ***\n")
        chunks = chunks[:100]  # This takes just the first 100 chunks
    # ----------------------------

    # 4. Initialize the embedding model
    model_kwargs = {'trust_remote_code': True}
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs
    )
    
    print(f"Embedding {len(chunks)} chunks... This will take some time.")
    
    # 5. Create the Chroma vector store
    vector_db = Chroma.from_documents(
        documents=chunks,  # This will now be the sliced list of 100
        embedding=embeddings, 
        persist_directory=VECTOR_DB_PATH
    )
    
    print(f"Vector store created successfully at {VECTOR_DB_PATH}")

def get_retriever():
    """
    Loads the existing vector store and returns a retriever object.
    This is the "Retrieval" step for the API.
    """
    
    # Initialize the *same* embedding model
    model_kwargs = {'trust_remote_code': True}
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs
    )
    
    # Load the persistent database from disk
    vector_db = Chroma(
        persist_directory=VECTOR_DB_PATH, 
        embedding_function=embeddings
    )
    
    # Create and return a retriever
    # 'k=5' means it will retrieve the top 5 most relevant chunks.
    return vector_db.as_retriever(search_kwargs={"k": 5})

# --- Test Block ---
if __name__ == "__main__":
    """
    If you run this file directly (e.g., 'python -m src.vector_store'),
    it will execute the ingestion process.
    """
    create_vector_store()