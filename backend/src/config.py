import os
from dotenv import load_dotenv

# --- Paths ---
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BACKEND_DIR, '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Target Repository (Unchanged) ---
TARGET_REPO_URL = "https://github.com/langchain-ai/langchain"
TARGET_REPO_PATH = os.path.join(BACKEND_DIR, "target_repo")

# --- Embedding Model (Unchanged) ---
EMBEDDING_MODEL_NAME = "nomic-ai/nomic-embed-text-v1"

# --- Vector Database (NEW) ---
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "chat-with-codebase" # You can name this anything

# --- LLM (NEW) ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# We're moving to a serverless architecture by integrating Pinecone, a cloud database, and Gemini API for LLM from the previous 
# idea of using Flask combined with a llama model downloaded locally 
# this'll help in deployment using a static hosts like vercel or netlify rather than using hosts like AWS which is more 
# powerful but expensive. 