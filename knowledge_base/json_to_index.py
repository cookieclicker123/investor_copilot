import os
import json
import faiss
import spacy
from sentence_transformers import SentenceTransformer

# Load the SpaCy model for English
nlp = spacy.load("en_core_web_sm")

def spacy_text_splitter(text, chunk_size, chunk_overlap):
    """Split text into chunks using SpaCy for sentence detection."""
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        
        if current_length + sentence_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = current_chunk[-chunk_overlap:]
            current_length = sum(len(s) for s in current_chunk)
        
        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def read_json_file(file_path):
    """Read a JSON file and return its content."""
    with open(file_path, "r") as file:
        return json.load(file)

def process_file(file_name, text_folder, splitter_params):
    """Process a single JSON file to extract text and metadata."""
    file_path = os.path.join(text_folder, file_name)
    data = read_json_file(file_path)
    text = data["text"]
    doc_metadata = data["metadata"]
    
    chunks = spacy_text_splitter(text, **splitter_params)
    metadatas = [
        {
            **doc_metadata,
            "chunk_id": i,
            "total_chunks": len(chunks),
            "chunk_size": len(chunk),
            "chunking_strategy": "dense" if splitter_params["chunk_size"] == 800 else "regular"
        }
        for i, chunk in enumerate(chunks)
    ]
    
    return chunks, metadatas

def load_and_split_texts(text_folder):
    """Load and split texts from JSON files in the specified folder."""
    dense_splitter_params = {"chunk_size": 800, "chunk_overlap": 400}
    regular_splitter_params = {"chunk_size": 1000, "chunk_overlap": 200}
    
    texts = []
    metadatas = []
    
    for file_name in os.listdir(text_folder):
        if file_name.endswith('.json'):
            is_dense_content = any(term in file_name.lower() for term in ['financial statement', 'balance sheet', 'income statement'])
            splitter_params = dense_splitter_params if is_dense_content else regular_splitter_params
            file_texts, file_metadatas = process_file(file_name, text_folder, splitter_params)
            texts.extend(file_texts)
            metadatas.extend(file_metadatas)
    
    return texts, metadatas

def create_faiss_index(text_folder, index_path, embedding_model='sentence-transformers/all-MiniLM-L6-v2'):
    """Create a FAISS index from text files."""
    texts, metadatas = load_and_split_texts(text_folder)
    model = SentenceTransformer(embedding_model)
    embeddings = model.encode(texts, convert_to_tensor=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.cpu().numpy())

    faiss.write_index(index, os.path.join(index_path, "faiss_index"))
    print(f"FAISS index saved to {index_path}")

if __name__ == "__main__":
    text_folder = "./data/processed"
    index_path = "./data/indexes"
    create_faiss_index(text_folder, index_path)
