from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


question = "What is the position of responsibility?"

results = vector_db.similarity_search(
    question,
    k=3
)


for i, doc in enumerate(results):

    print("\n====================")
    print(f"RESULT {i + 1}")
    print("====================")

    print(doc.page_content)