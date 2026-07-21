import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

EXCEL_FILE = "datasets/EXIM_AI_Engineer_Simulated_Data.xlsx"

DB_PATH = "chroma_db"
COLLECTION_NAME = "excel_knowledge"

print("=" * 50)
print("Loading Embedding Model...")
print("=" * 50)

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_PATH)

# -------------------------
# Delete old data
# -------------------------

try:
    client.delete_collection(COLLECTION_NAME)
    print("Old collection deleted.")
except:
    pass

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

# -------------------------
# Read Excel
# -------------------------

excel = pd.ExcelFile(EXCEL_FILE)

print("\nSheets Found:")

for sheet in excel.sheet_names:
    print("-", sheet)

print()

total_rows = 0

# -------------------------
# Read every sheet
# -------------------------

for sheet in excel.sheet_names:

    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

    df = df.fillna("")

    ids = []
    docs = []
    metas = []

    for index, row in df.iterrows():

        text = f"Sheet: {sheet}\n\n"

        for column in df.columns:
            text += f"{column}: {row[column]}\n"

        ids.append(f"{sheet}_{index}")

        docs.append(text)

        metas.append({
            "sheet": sheet,
            "row": index
        })

    if docs:

        embeddings = model.encode(
            docs,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False
        ).tolist()

        BATCH_SIZE = 5000

        for i in range(0, len(ids), BATCH_SIZE):

            collection.add(
                ids=ids[i:i+BATCH_SIZE],
                documents=docs[i:i+BATCH_SIZE],
                embeddings=embeddings[i:i+BATCH_SIZE],
                metadatas=metas[i:i+BATCH_SIZE]
            )

        total_rows += len(docs)

        print(f"{sheet} -> {len(docs)} rows indexed")

print("\n" + "=" * 50)
print("Excel Index Complete")
print("=" * 50)
print("Total Rows:", total_rows)
print("Collection:", COLLECTION_NAME)