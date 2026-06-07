import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "vector_store/policy_chroma"
COLLECTION_NAME = "supply_chain_policy"


def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    print("\nPolicy RAG Search")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a policy question: ")

        if question.lower() == "exit":
            print("Goodbye.")
            break

        query_embedding = model.encode([question]).tolist()[0]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )

        print("\nRetrieved Policy Context:")
        for doc in results["documents"][0]:
            print("\n---")
            print(doc)


if __name__ == "__main__":
    main()