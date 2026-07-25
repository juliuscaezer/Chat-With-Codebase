import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum

# --- UPDATED PATH RESOLUTION ---
# Since chat.py is inside backend/src, we go up ONE level to 'backend'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR) 
sys.path.append(BACKEND_DIR)

# Import your RAG chain using the correct function name
try:
    from src.rag_pipeline import create_rag_chain
except ImportError as e:
    print(f"Error importing RAG pipeline: {e}")
    def create_rag_chain():
        return None

app = FastAPI(title="Chat with Codebase API")

# Configure CORS (You'll update this with your CloudFront/S3 domain later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the RAG chain globally
rag_chain = create_rag_chain()

# Define the expected request body using Pydantic
class ChatRequest(BaseModel):
    question: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not rag_chain:
        raise HTTPException(status_code=500, detail="RAG chain is not loaded.")
        
    try:
        print(f"Received question: {request.question}")
        
        # Invoke the RAG chain
        response = rag_chain.invoke(request.question)
        
        return {"answer": response}
        
    except Exception as e:
        print(f"Error in /api/chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Wrap the FastAPI app with Mangum for AWS Lambda compatibility
handler = Mangum(app)

# Local testing block
if __name__ == "__main__":
    import uvicorn
    print("\n--- RUNNING IN LOCAL TEST MODE (FastAPI) ---")
    uvicorn.run(app, host="127.0.0.1", port=5001)