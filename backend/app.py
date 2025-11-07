import os 
from flask import Flask, request, jsonify
from flask_cors import CORS 

# --- Configuration ---
# (We will add our RAG logic imports here later)

app = Flask(__name__)

# --- CORS (Cross-Origin Resource Sharing) ---
# This is a *crucial* security step that allows your React app (e.g., http://localhost:3000)
# to make requests to your Flask server (e.g., http://localhost:5000).
CORS(app, resources={r"/api/*":{"origins":"https://localhost:3000"}})

# API Endpoints 

@app.route('/api/test', methods=['GET'])

def test_connection():
    # A test endpoint to see if server is running 
    return jsonify({"message":"Flask server is connected"}), 200

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    # The main endpoint for our application

    # The 'OPTIONS' method is automatically handled by flask_cors
    # to check if the 'POST' request is allowed.

    if request.method == 'POST':
        try:
            data = request.json
            question = data.get('question')

            if not question:
                return jsonify({"error":"No question provided"}), 400
        
            # --- DUMMY RAG LOGIC ---
            # Right now, we will just echo the question back with a dummy answer.
            # In the next step, we will replace this with our REAL RAG pipeline.

            print(f"Received question: {question}") # For debugging 
            dummy_answer = f"This is a dummy answer for your question: '{question}'"

            return jsonify({"answer":dummy_answer})
        
        except Exception as e:
            print(f"Error in /api/chat: {e}")
            return jsonify({"error":"Internal Server Error"}), 500
        
# --- Main Execution ---
if __name__ == '__main__':
    # We will use Gunicorn for production, but the 'flask run' command is best for development.
    # To run this, you will use the command: flask run
    # (It will default to port 5000)
    app.run(debug=True) # debug=True will auto-reload the server when you save the file

