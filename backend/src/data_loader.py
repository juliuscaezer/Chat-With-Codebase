import os
import git  # <-- The correct library for cloning
from langchain_community.document_loaders import GitLoader

# We import our settings directly from our config file
from src.config import TARGET_REPO_URL, TARGET_REPO_PATH

def load_git_repo():
    """
    Clones the target repository if it doesn't exist,
    and loads all specified files into memory as LangChain 'Documents'.
    """
    
    # 1. Check if the repo is already cloned
    if os.path.exists(TARGET_REPO_PATH):
        print(f"Repository already exists at: {TARGET_REPO_PATH}")
    else:
        print(f"Cloning repository from {TARGET_REPO_URL} to {TARGET_REPO_PATH}...")
        # Note: This might take a few minutes the first time!
        try:
            # --- THIS IS THE FIX ---
            # We use the 'git' library to clone the repo
            git.Repo.clone_from(
                url=TARGET_REPO_URL,
                to_path=TARGET_REPO_PATH,
                branch="master" # You can change this to 'main' or any other branch
            )
            # -----------------------
            print("Repository cloned successfully.")
        except Exception as e:
            print(f"Error cloning repository: {e}")
            return [] # Return an empty list on failure

    # 2. Now, load the files from the cloned repo
    # This part of the logic was correct before.
    print("Loading files from repository...")
    loader = GitLoader(
        repo_path=TARGET_REPO_PATH,
        branch="master",
        # This filter is critical:
        file_filter=lambda file_path: file_path.endswith(
            (".py", ".js", ".jsx", ".ts", ".tsx", ".md", ".json", ".html", ".css")
        )
    )

    try:
        data = loader.load()
        if not data:
            print("No files matching the filter were found in the repository.")
            return []
        print(f"Loaded {len(data)} documents from the repository.")
        return data
    except Exception as e:
        print(f"Error loading files from repository: {e}")
        return []

# --- This is a good way to test the file directly ---
if __name__ == "__main__":
    """
    If you run this file directly (e.g., 'python -m src.data_loader'),
    it will execute this block of code.
    """
    print("Running data loader test...")
    documents = load_git_repo()
    if documents:
        print(f"\n--- Example Document (First 500 chars) ---")
        print(documents[0].page_content[:500])
        print("---------------------------------------------")
        print(f"Path: {documents[0].metadata.get('file_path')}")
    else:
        print("No documents loaded.")