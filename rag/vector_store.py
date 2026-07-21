import json
import chromadb
from sentence_transformers import SentenceTransformer

CHUNK_FILE = "rag/chunks.json"
DB_PATH = "chroma_db"
COLLECTION_NAME = "logistics_documents"
BATCH_SIZE = 100

print("=" * 50)
print("Loading Embedding Model...")
print("=" * 50)

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

# -----------------------------
# Delete existing vectors
# -----------------------------
existing = collection.get()

if existing["ids"]:
    print(f"Deleting {len(existing['ids'])} old vectors...")
    collection.delete(ids=existing["ids"])

print("\nLoading chunks...")

with open(CHUNK_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Remove empty chunks
chunks = [c for c in chunks if c["chunk_content"].strip()]

print(f"Total Chunks Found : {len(chunks)}")

total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE

print("\nStarting Indexing...\n")

for batch_number in range(total_batches):

    start = batch_number * BATCH_SIZE
    end = min(start + BATCH_SIZE, len(chunks))

    batch = chunks[start:end]

    texts = [c["chunk_content"] for c in batch]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False
    ).tolist()

    ids = []
    docs = []
    metas = []

    for chunk in batch:

        ids.append(chunk["chunk_id"])
        docs.append(chunk["chunk_content"])

        metas.append({
            "chunk_id": chunk["chunk_id"],
            "document_name": chunk["document_name"],
            "document_type": chunk["metadata"].get("document_type", ""),
            "chunk_number": chunk["metadata"].get("chunk_number", 1),
            "source": chunk["metadata"].get("source_folder", "")
        })

    collection.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metas
    )

    print(f"Batch {batch_number+1}/{total_batches} Indexed ({end}/{len(chunks)})")

print("\n" + "=" * 50)
print("ChromaDB Knowledge Base Created")
print("=" * 50)
print("Documents Indexed :", len(set(c["document_name"] for c in chunks)))
print("Chunks Indexed    :", collection.count())
print("Embedding Model   : all-MiniLM-L6-v2")
print("=" * 50)
print("Knowledge Base Ready")
print("=" * 50)