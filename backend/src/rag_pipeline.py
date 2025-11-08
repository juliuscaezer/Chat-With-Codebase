from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.config import OPENAI_API_KEY
from src.vector_store import get_retriever
def create_rag_chain():
    """
    Creates the main RAG chain for answering questions.
    """

    # Load vector store from disk
    retriever = get_retriever()

    # Define the LLM 
    # Change the LLM to Groq/Mistral
    llm = ChatOpenAI(
        api_key = OPENAI_API_KEY,
        model = "gpt-3.5-turbo"
    )

    # 3. Define the Prompt Template
    # This is where we "stuff" the context (the code chunks)
    # in front of the user's question.
    template = """
    You are an expert software developer assistant.
    Answer the user's question based ONLY on the following context of code snippets
    and documentation. If the context does not contain the answer,
    state clearly that you cannot answer from the provided information.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        # Function to combine all retrieved chunks 
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context":retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

if __name__ == "__main__":
    """
    If you run this file directly (e.g., 'python -m src.rag_pipeline'),
    it will execute this block.
    """
    print("Running RAG pipeline test...")
    
    # Make sure your .env file has your OPENAI_API_KEY
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found. Please set it in your .env file.")
    else:
        chain = create_rag_chain()
        
        # Test with a question
        question = "How is authentication handled in this repository?"
        print(f"Testing with question: '{question}'")
        
        response = chain.invoke(question)
        
        print("\n--- RAG Response ---")
        print(response)