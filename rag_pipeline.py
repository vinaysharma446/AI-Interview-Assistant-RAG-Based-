from rag_engine import split_text, create_vector_store, retrieve

# 🔹 Load knowledge base
def load_knowledge_base(file_path="data/interview_qa.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = split_text(text)
    index, chunks = create_vector_store(chunks)

    return index, chunks

# 🔹 Retrieve from knowledge base
def retrieve_knowledge(query, index, chunks):
    return retrieve(query, index, chunks, k=3)