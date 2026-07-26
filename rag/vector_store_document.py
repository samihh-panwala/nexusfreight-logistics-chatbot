import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("✅ Connected to Supabase")

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model loaded")

DOCUMENT_FOLDER = "documents"

CHUNK_SIZE = 500
OVERLAP = 100

def chunk_text(text, chunk_size=500, overlap=100):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def read_documents():

    all_chunks = []

    document_path = Path(DOCUMENT_FOLDER)

    txt_files = list(document_path.glob("*.txt"))

    print(f"\nFound {len(txt_files)} text files.\n")

    for file in txt_files:

        print(f"Reading {file.name}")

        with open(file, "r", encoding="utf-8", errors="ignore") as f:

            text = f.read()

        chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)

        print(f"   {len(chunks)} chunks created")

        for i, chunk in enumerate(chunks):

            all_chunks.append({

                "chunk_id": f"{file.stem}_chunk_{i+1}",

                "document_name": file.name,

                "document_type": file.stem,

                "chunk_number": i + 1,

                "content": chunk,

                "metadata": {

                    "source_folder": "documents",

                    "chunk_number": i + 1,

                    "document_type": file.stem

                }

            })

    return all_chunks

def upload_chunks(chunks):

    BATCH_SIZE = 100

    total = len(chunks)

    print(f"\nUploading {total} chunks...\n")

    for i in tqdm(range(0, total, BATCH_SIZE)):

        batch = chunks[i:i+BATCH_SIZE]

        records = []

        for chunk in batch:

            embedding = model.encode(chunk["content"]).tolist()

            records.append({

                "id": str(uuid.uuid4()),

                "chunk_id": chunk["chunk_id"],

                "document_name": chunk["document_name"],

                "document_type": chunk["document_type"],

                "chunk_number": chunk["chunk_number"],

                "content": chunk["content"],

                "embedding": embedding,

                "metadata": chunk["metadata"]

            })

        supabase.table("document_embeddings").insert(records).execute()

    print("\n✅ Upload Completed")
    


#####
if __name__ == "__main__":

    chunks = read_documents()

    print("\nTotal Chunks:", len(chunks))

    upload_chunks(chunks)