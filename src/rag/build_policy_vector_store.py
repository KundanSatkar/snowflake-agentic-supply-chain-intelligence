from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

POLICY_PATH = Path("data/synthetic_docs/supply_chain_policy.md")
CHROMA_PATH = "vector_store/policy_chroma"
COLLECTION_NAME = "supply_chain_policy"


def chunk_text(text):
    sections = text.split("##")
    chunks = []

    for section in sections:
        section = section.strip()
        if section:
            chunks.append(section)

    return chunks


def main():
    print("Loading policy document...")
    policy_text = POLICY_PATH.read_text()

    print("Chunking document...")
    chunks = chunk_text(policy_text)

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating embeddings...")
    embeddings = model.encode(chunks).tolist()

    print("Creating ChromaDB vector store...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    ids = [f"policy_chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print("Vector store created successfully.")
    print(f"Saved to: {CHROMA_PATH}")


if __name__ == "__main__":
    main()