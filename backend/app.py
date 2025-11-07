import os
from flask import Flask, request, jsonify
from flask_cors import CORS # This is the critical import

# --- Configuration ---
# (We will add our RAG logic imports here later)

# Initialize the Flask app
app = Flask(__name__)

# --- CORS (Cross-Origin Resource Sharing) ---
# This is a *crucial* security step that allows your React app (e.g., http://localhost:3000)
# to make requests to your Flask server (e.g., http://localhost:5000).
# We are only allowing requests from our React app's origin.
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


# --- API Endpoints ---

@app.route('/api/test', methods=['GET'])
def test_connection():
    """
    A simple test endpoint to check if the server is running.
    """
    return jsonify({"message": "Flask server is connected!"}), 200

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """
    The main endpoint for our chatbot.
    """
    # The 'OPTIONS' method is automatically handled by flask_cors
    # to check if the 'POST' request is allowed.
    if request.method == 'POST':
        try:
            data = request.json
            question = data.get('question')

            if not question:
                return jsonify({"error": "No question provided"}), 400

            # --- DUMMY RAG LOGIC ---
            # Right now, we will just echo the question back with a dummy answer.
            # In the next step, we will replace this with our REAL RAG pipeline.
            print(f"Received question: {question}") # For debugging in our terminal
            dummy_answer = f"This is a dummy answer for your question: '{question}'"
            # -------------------------

            return jsonify({"answer": dummy_answer}), 200

        except Exception as e:
            print(f"Error in /api/chat: {e}")
            return jsonify({"error": "Internal server error"}), 500

# --- Main execution ---
if __name__ == '__main__':
    # This block is not strictly necessary for 'flask run', 
    # but it's good practice. We're telling Flask to run in "debug" mode,
    # which will automatically reload the server every time you save the file.
    app.run(debug=True, host='0.0.0.0', port=5000)