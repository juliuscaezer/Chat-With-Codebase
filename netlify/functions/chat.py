import json
import os
import sys
from mangum import Mangum
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- vvv THIS IS THE FIX vvv ---
# We must go up TWO levels from 'functions' to get to the root,
# then go down into 'backend'.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# SCRIPT_DIR is '.../netlify/functions'
# '..' goes to '.../netlify'
# '..' goes to '.../chat-with-codebase-pro'
# 'backend' goes to '.../chat-with-codebase-pro/backend'
BACKEND_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'backend')
sys.path.append(BACKEND_DIR)
# --- ^^^ THIS IS THE FIX ^^^ ---

# Now, this import will work
try:
    # Python looks in 'backend/src/rag_pipeline.py'
    from src.rag_pipeline import create_rag_chain
except ImportError:
    print(f"Error: Could not import 'create_rag_chain'.")
    print(f"Attempted to add this path: {BACKEND_DIR}")
    print("Current Python Path:", sys.path)
    def create_rag_chain():
        return None

app = Flask(__name__)
# Allow requests ONLY from our React dev server
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
try:
    rag_chain = create_rag_chain()
    print("RAG chain loaded successfully.")
except Exception as e:
    print(f"Error loading RAG chain: {e}")
    rag_chain = None

@app.route('/api/chat', methods=['POST'])
def chat():
    if not rag_chain:
        return jsonify({"error": "RAG chain is not loaded."}), 500
        
    try:
        data = request.json
        question = data.get('question')

        if not question:
            return jsonify({"error": "No question provided"}), 400

        print(f"Received question: {question}")
        
        response = rag_chain.invoke(question)

        return jsonify({"answer": response}), 200

    except Exception as e:
        print(f"Error in /api/chat: {e}")
        return jsonify({"error": "Internal server error"}), 500

handler = Mangum(app)

# --- LOCAL TEST BLOCK ---
# ... (at the very bottom of the file) ...

# --- LOCAL TEST BLOCK ---
"""if __name__ == "__main__":
    try:
        from src.config import GOOGLE_API_KEY
        if not GOOGLE_API_KEY:
            print("FATAL: GOOGLE_API_KEY not found in .env file.")
        else:
            print("\n--- RUNNING IN LOCAL TEST MODE ---")
            print("--- Access this server at http://127.0.0.1:5001 ---")
            app.run(debug=True, port=5001)
    except ImportError:
        print("\nError: Could not import config.")"""