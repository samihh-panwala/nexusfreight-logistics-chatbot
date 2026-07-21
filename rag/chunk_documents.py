import os
import json

# ----------------------------------
# Folders containing knowledge files
# ----------------------------------

DOCUMENT_FOLDERS = [
    "documents",
    "documents_old"
]

OUTPUT_FILE = "rag/chunks.json"

CHUNK_SIZE = 200  # words per chunk

# ----------------------------------
# Function to split text into chunks
# ----------------------------------

def chunk_text(text, chunk_size=200, overlap=50):

    words = text.split()

    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):

        chunk = words[i:i + chunk_size]

        if chunk:
            chunks.append(" ".join(chunk))

    return chunks


all_chunks = []
processed_files = 0

# ----------------------------------
# Read all TXT and MD files
# ----------------------------------

for folder in DOCUMENT_FOLDERS:

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        continue

    for filename in os.listdir(folder):

        if filename.endswith(".txt") or filename.endswith(".md"):

            processed_files += 1

            filepath = os.path.join(folder, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()

            # Skip empty files
            if not text.strip():
                print(f"Skipped empty file: {filename}")
                continue

            chunks = chunk_text(text, CHUNK_SIZE)

            document_type = os.path.splitext(filename)[0]

            for index, chunk in enumerate(chunks):

                chunk_data = {
                    "chunk_id": f"{document_type}_chunk_{index + 1}",
                    "document_name": filename,
                    "chunk_content": chunk,
                    "metadata": {
                        "document_type": document_type,
                        "source_folder": folder,
                        "chunk_number": index + 1,
                    }
                }

                all_chunks.append(chunk_data)

# ----------------------------------
# Save chunks to JSON
# ----------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(all_chunks, file, indent=4)

# ----------------------------------
# Summary
# ----------------------------------

print("=" * 45)
print(" Document Chunking Completed")
print("=" * 45)
print(f"Documents Processed : {processed_files}")
print(f"Total Chunks Created: {len(all_chunks)}")
print(f"Saved to : {OUTPUT_FILE}")
print("=" * 45)