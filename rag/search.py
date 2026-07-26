import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("✅ Supabase Connected")

print("Loading embedding model...")

model = None

def get_model():
    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded.")

    return model

print("✅ Embedding Model Loaded")


def search_documents(query, top_k=5):

    embedding_model = get_model()

    embedding = embedding_model.encode(query).tolist()

    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": embedding,
            "match_count": top_k
        }
    ).execute()

    documents = []

    for row in response.data:

        documents.append({

            "chunk_id": row["chunk_id"],

            "document": row["content"],

            "metadata": {

                "document_name": row["document_name"],

                "document_type": row["document_type"],

                "chunk_number": row["chunk_number"]

            },

            "source": row["document_name"],

            "distance": 1 - row["similarity"],

            "keyword_score": 1

        })

    return documents