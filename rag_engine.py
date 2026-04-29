from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔹 Split text
def split_text(text, chunk_size=200):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# 🔹 Create vector store
def create_vector_store(chunks):
    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index, chunks

# 🔹 Retrieve
def retrieve(query, index, chunks, k=3):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k)

    return [chunks[i] for i in indices[0]]