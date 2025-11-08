from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.config import GOOGLE_API_KEY
from src.vector_store import get_retriever # Pinecone Retriever 

def create_rag_chain():
    """
    Creates the main RAG chain for answering questions using Google Gemini.
    """
    
    # 1. Get the retriever
    # This now loads our PINECODE retriever
    retriever = get_retriever()

    # 2. Define the LLM 
    llm = ChatGoogleGenerativeAI(
        google_api_key = GOOGLE_API_KEY,
        model = "gemini-2.5-flash"
    )

    # 3. Define the Prompt Template
    # This prompt is slightly tuned for Gemini
    template = """
    You are an expert software developer assistant.
    Answer the user's question based ONLY on the following context.
    If the context does not contain the answer, state clearly that you cannot
    find the answer in the provided context.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    
    prompt = ChatPromptTemplate.from_template(template)

    # 4. Build the RAG Chain (This logic is identical to before)
    
    def format_docs(docs):
        # A helper function to combine all the retrieved chunks
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# --- Test Block ---
if __name__ == "__main__":
    """
    If you run this file directly (e.g., 'python -m src.rag_pipeline'),
    it will test the full serverless RAG pipeline.
    """
    print("Running Serverless RAG pipeline test (Pinecone + Gemini)...")
    
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found. Please set it in your .env file.")
    else:
        chain = create_rag_chain()
        
        # Test with a question
        question = "What is the repository about?"
        print(f"Testing with question: '{question}'")
        
        try:
            response = chain.invoke(question)
            
            print("\n--- RAG Response (Gemini) ---")
            print(response)
        except Exception as e:
            print(f"\n--- An error occurred ---")
            print(e)

