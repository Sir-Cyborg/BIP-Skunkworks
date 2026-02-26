# test.py

from retriever import Retriever

def main():
    print("Initializing retriever...")
    retriever = Retriever()

    print("Checking collection count...")
    count = retriever.collection.count()
    print(f"Number of documents in collection: {count}")

    if count == 0:
        print("⚠️ Collection is empty. Add documents first.")
        return

    print("\nRunning test query...\n")

    try:
        context = retriever.retrieve("test")
        print("Retrieved Context:\n")
        print(context)
    except Exception as e:
        print("❌ Error during retrieval:")
        print(type(e).__name__, e)

if __name__ == "__main__":
    main()