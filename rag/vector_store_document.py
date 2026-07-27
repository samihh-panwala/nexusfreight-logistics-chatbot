import os
import uuid
import time
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client
from tqdm import tqdm

from providers.jina_embedding import get_embedding

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

DOCUMENT_FOLDER = "documents"

CHUNK_SIZE = 200
OVERLAP = 40

UPLOAD_BATCH_SIZE = 20
BATCH_SLEEP = 10


def chunk_text(text):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + CHUNK_SIZE

        chunks.append(" ".join(words[start:end]))

        start += CHUNK_SIZE - OVERLAP

    return chunks


def read_documents():

    all_chunks = []

    txt_files = list(Path(DOCUMENT_FOLDER).glob("*.txt"))

    print(f"\nFound {len(txt_files)} text files.\n")

    for file in txt_files:

        print(f"Reading {file.name}")

        with open(file, "r", encoding="utf-8", errors="ignore") as f:

            text = f.read()

        chunks = chunk_text(text)

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


def chunk_exists(chunk_id):
    response = (
        supabase
        .table("document_embeddings")
        .select("chunk_id")
        .eq("chunk_id", chunk_id)
        .limit(1)
        .execute()
    )

    return len(response.data) > 0

def upload_chunks(chunks):

    total = len(chunks)

    print(f"\nUploading {total} chunks...\n")

    for batch_start in tqdm(range(0, total, UPLOAD_BATCH_SIZE)):

        batch = chunks[batch_start:batch_start + UPLOAD_BATCH_SIZE]

        records = []

        for chunk in batch:

            while True:

                try:
                    
                    # Skip already uploaded chunks
                    if chunk_exists(chunk["chunk_id"]):
                        print(f"Skipping {chunk['chunk_id']}")
                        continue
                    embedding = get_embedding(chunk["content"])

                    break

                except Exception as e:

                    print(f"\nEmbedding Error: {e}")

                    print("Waiting 60 seconds...")

                    time.sleep(60)

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

        while True:

            try:

                if records:
                    supabase.table("document_embeddings").insert(records).execute()

                break

            except Exception as e:

                print(f"\nUpload Error: {e}")

                print("Retrying in 30 seconds...")

                time.sleep(30)

        print(f"Uploaded {min(batch_start + UPLOAD_BATCH_SIZE, total)} / {total}")

        time.sleep(BATCH_SLEEP)

    print("\n✅ Upload Completed")


if __name__ == "__main__":

    chunks = read_documents()

    print(f"\nTotal Chunks: {len(chunks)}")

    upload_chunks(chunks)