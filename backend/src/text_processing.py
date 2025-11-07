import os
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language
)

from src.data_loader import load_git_repo

def split_code_documents(documents):
    """
    Splits a list of LangChain Documents into smaller chunks.
    It uses a Python-specific splitter for .py files,
    a Markdown-specific one for .md files,
    and a generic one for all other file types.
    """
    print(f"Splitting {len(documents)} documents into chunks...")

    # Initial code splitters for now - Python, Markdown, Generic Splitter

    # Chunk Size and Overlap are hard coded, must make them dynamic based on code 

    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language = Language.PYTHON,
        chunk_size = 1000, # Max size of a chunk (in characters)
        chunk_overlap = 200, # How many characters to overlap between chunks
    )

    markdown_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN,
        chunk_size = 1000,
        chunk_overlap = 200 
    )
    
    generic_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    # --- Logic to Split Documents ---
    split_docs = []
    files_processed = 0

    for doc in documents:
        # We need filepath to decide which splitter to use 
        file_path = doc.metadata.get("file_path")
        if file_path and file_path.endswith(".py"):
            chunks = python_splitter.split_documents([doc])
        elif file_path and file_path.endswith(".md"):
            chunks = markdown_splitter.split_documents([doc])
        else:
            # For .json, .html, .css, etc.
            chunks = generic_splitter.split_documents([doc])
            
        split_docs.extend(chunks)
        
        files_processed += 1
        if files_processed % 500 == 0 or files_processed == len(documents):
            print(f"Processed {files_processed} / {len(documents)} files...")
    
    print(f"Original documents: {len(documents)}. Total chunks: {len(split_docs)}")
    return split_docs

# --- Test Block ---
if __name__ == "__main__":
    """
    If you run this file directly (e.g., 'python -m src.text_processing'),
    it will execute this block.
    """
    print("Running text processing test...")
    
    # 1. First, load the documents
    documents = load_git_repo()
    
    if documents:
        # 2. Then, split them
        chunks = split_code_documents(documents)
        
        if chunks:
            print("\n--- Example Chunk (from a Python file) ---")
            # Let's find a Python chunk to show as an example
            py_chunk_example = "No Python chunks found in sample."
            for chunk in chunks:
                 if chunk.metadata.get("file_path", "").endswith(".py"):
                    py_chunk_example = chunk.page_content
                    print(py_chunk_example)
                    print("---------------------")
                    print(f"Metadata: {chunk.metadata}")
                    break
    else:
        print("No documents found by data loader.")
