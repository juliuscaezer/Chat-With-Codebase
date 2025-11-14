# Chat with Codebase 

This is a full-stack, serverless RAG (Retrieval-Augmented Generation) application that allows you to ask natural language questions about a specific GitHub repository.

It leverages a 100% serverless architecture to provide in-depth, context-aware answers about the repository.

## Features

  * **Conversational AI:** A clean, fast React-based chat interface.
  * **Serverless RAG Pipeline:** A 100% serverless backend that runs on Netlify, ensuring scalable deployment.
  * **Deep Code Awareness:** Ingests an entire codebase, splitting it semantically (by functions/classes) to provide accurate, context-aware answers.
  * **Cloud-Native:** Uses Pinecone for persistent, cloud-based vector storage and Google Gemini for state-of-the-art text generation.

## Tech Stack

This project is a "monorepo" with a separate frontend and backend.

### Frontend

  * **Framework:** React (using Vite)
  * **UI:** Plain CSS
  * **API Client:** Axios
  * **Host:** Netlify

### Backend & RAG Pipeline

  * **API:** Python + Flask (run as a serverless function via `Mangum`)
  * **LLM:** Google Gemini (`gemini-1.5-flash`)
  * **Vector Database:** Pinecone (Serverless, Cloud-based)
  * **Embedding Model:** `nomic-ai/nomic-embed-text-v1`
  * **Data Handling:** LangChain
  * **Host:** Netlify Functions

## Getting Started (Local Development)

To run this project on your local machine, you will need to run the frontend and backend in two separate terminals.

### Prerequisites

  * [Node.js](https://nodejs.org/en)
  * [Python 3.10+](https://www.python.org/)
  * [Git](https://git-scm.com/)
  * **Pinecone API Key:** Get one from [Pinecone](https://www.pinecone.io/)
  * **Google API Key:** Get one from [Google AI Studio](https://aistudio.google.com/app/apikey)

-----

### 1\. Clone the Repository

```bash
git clone https://github.com/juliuscaezer/chat-with-codebase.git
cd chat-with-codebase-pro
```

### 2\. Configure Environment Variables

1.  Navigate into the `backend/` folder.
2.  Create a file named `.env`:
    ```bash
    # /backend/.env

    PINECONE_API_KEY="YOUR_PINECONE_API_KEY"
    GOOGLE_API_KEY="YOUR_GOOGLE_AI_KEY"
    ```

### 3\. Set Up the Backend

```bash
# From the /backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install all Python dependencies
pip install -r requirements.txt
```

### 4\. Set Up the Frontend

```bash
# From the root folder, go into the frontend
cd ../frontend

# Install all Node modules
npm install
```

### 5\. Run the Data Ingestion

Before you can chat, you must load the codebase data into your Pinecone database.

1.  Make sure you are in the `backend/` folder with your `(venv)` active.
2.  Open `backend/src/vector_store.py` and set `TEST_MODE = True` (to ingest 500 chunks) or `False` (for the full 16,000+ chunks).
3.  Run the ingestion script:
    ```bash
    # This will clone the repo, split the files, and upload
    # all embeddings to Pinecone. This may take 10-15 minutes.
    python -m src.vector_store
    ```

### 6\. Run the Project (Two-Terminal Mode)

You are now ready to run the app.

  * **Terminal 1 (Run the Backend API):**

    ```bash
    # Start from the /backend folder (with venv active)

    # This runs our Netlify function as a local test server
    python ../netlify/functions/chat.py

    # You should see it running on http://127.0.0.1:5001
    ```

  * **Terminal 2 (Run the Frontend UI):**

    ```bash
    # Start from the /frontend folder
    npm run dev

    # Your browser will open to http://localhost:5173
    ```

You can now use the app in your browser\!

-----

## Deployment

This project is built to deploy **for free** on Netlify. This is one of the main reasons to keep the project serverless. Another recommended alternative for a server based version of this will be to use Flask combined with a vector database like ChromaDB instead of Pinecone (cloud storage) and a model like Llama which can be downloaded locally as a substitute for Gemini. However that will demand server based hosting facilities like AWS, Azure, etc. 

### 1\. Final Code Prep

Before pushing, make sure you have done the following:

1.  **Clean `chat.py`:** Remove the `if __name__ == "__main__":` local test block from `netlify/functions/chat.py`.
2.  **Fix `App.jsx` URL:** Change the `API_URL` variable in `frontend/src/App.jsx` to the relative path:
    ```jsx
    const API_URL = '/api/chat';
    ```

### 2\. Push to GitHub

Commit all your changes and push them to your main branch.

```bash
git add .
git commit -m "feat: Prepare for production deployment"
git push origin main
```

### 3\. Deploy on Netlify

1.  Log in to Netlify and connect your GitHub repository.
2.  Netlify will automatically read your `netlify.toml` file and apply these settings:
      * **Base directory:** `frontend`
      * **Build command:** `npm run build`
      * **Publish directory:** `frontend/dist`
3.  **Add Environment Variables:** Go to **Site settings \> Build & deploy \> Environment** and add your two secret keys:
      * `GOOGLE_API_KEY`: `AIzaSy...`
      * `PINECONE_API_KEY`: `your-pinecone-key...`
4.  Click **"Deploy site"**. Netlify will build your React app, set up your Python serverless function, and launch your site.

