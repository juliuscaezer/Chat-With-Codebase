import os 
from dotenv import load_dotenv

# Find the root directory of the 'backend' folder
# This allows us to build absolute paths, which is safer than relative paths
# __file__ is the current file (config.py)
# os.path.dirname() goes "up" one folder
# So, BACKEND_DIR will be '.../chat-with-codebase-pro/backend'
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file in the 'backend' folder 
dotenv_path = os.path.join(BACKEND_DIR, '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Target Repository ---
# The repo we want to chat with
TARGET_REPO_URL = "https://github.com/langchain-ai/langchain" # <-- You can change this
# Where we will clone it to
TARGET_REPO_PATH = os.path.join(BACKEND_DIR, "target_repo")

# --- Vector Database ---
# Where we will store the ChromaDB vector database
VECTOR_DB_PATH = os.path.join(BACKEND_DIR, "db")

# --- Embedding Model ---
# The model we'll use to create vector embeddings
# This is a great, lightweight, and powerful open-source model.
EMBEDDING_MODEL_NAME = "nomic-ai/nomic-embed-text-v1"

# --- LLM API Keys ---
# Load your API key from the .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# You could add ANTHROPIC_API_KEY, GOOGLE_API_KEY, etc. here