import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Any
import logging
from utils.config import Config

# Disable logging for the transformers and FAISS
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
logging.getLogger('faiss').setLevel(logging.WARNING)

# Initialize configuration
config = Config.path_config
index_path = config.index_dir
embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'
device = 'mps'  # Change to 'cuda' if you have a GPU

# Load the Sentence Transformer model
model = SentenceTransformer(embedding_model, device=device)

# Load the FAISS index
index = faiss.read_index(os.path.join(index_path, "faiss_index"))

def get_context(query: str, k: int = 5) -> str:
    """Retrieve relevant context for a query."""
    try:
        # Encode the query to get its embedding
        query_embedding = model.encode([query], convert_to_tensor=True).cpu().numpy()
        print(f"Query embedding: {query_embedding}")  # Debugging statement

        # Search the FAISS index
        distances, indices = index.search(query_embedding, k)
        print(f"Retrieved indices: {indices}, distances: {distances}")  # Debugging statement

        # Retrieve and format the documents
        docs = retrieve_documents(indices)
        print(f"Retrieved documents: {docs}")  # Debugging statement
        return format_context(docs)
    except Exception as e:
        raise Exception(f"Error retrieving context: {str(e)}")

def retrieve_documents(indices: np.ndarray) -> List[Any]:
    """Retrieve documents based on indices from the FAISS index."""
    docs = []
    for idx in indices[0]:  # Assuming indices is a 2D array
        # Retrieve actual document content based on index
        # Example: doc_content = get_document_content(idx)
        doc_content = get_document_content(idx)  # Replace with actual content retrieval logic
        doc = {
            "metadata": {"source": f"Document {idx}"},
            "page_content": doc_content
        }
        print(f"Retrieving document for index {idx}: {doc}")  # Debugging statement
        docs.append(doc)
    return docs

def get_document_content(idx: int) -> str:
    """Fetch the actual content of a document given its index."""
    # Implement logic to fetch content from your data source
    # Example: return document_data[idx]
    return f"Actual content for document {idx}"  # Placeholder for actual retrieval logic

def format_context(docs: List[Any]) -> str:
    """Format retrieved documents into a string."""
    context_parts = []
    for i, doc in enumerate(docs, 1):
        metadata = doc["metadata"]
        context_parts.append(
            f"Document {i}:\n"
            f"Source: {metadata.get('source', 'Unknown')}\n"
            f"Content: {doc['page_content']}\n"
        )
    return "\n".join(context_parts)

def query_documents(query: str) -> str:
    """Query the processed documents."""
    return get_context(query)
