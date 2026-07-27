import os
from dotenv import load_dotenv
from supabase import create_client

from providers.jina_embedding import get_embedding

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("✅ Supabase Connected")


def search_documents(query, top_k=5):

    print("Generating Jina embedding...")

    embedding = get_embedding(query)

    print("Searching Supabase...")

    response = (
        supabase.rpc(
            "match_documents",
            {
                "query_embedding": embedding,
                "match_count": top_k,
            },
        ).execute()
    )

    documents = []

    if response.data:

        for row in response.data:

            documents.append(
                {
                    "chunk_id": row["chunk_id"],
                    "document": row["content"],
                    "metadata": {
                        "document_name": row["document_name"],
                        "document_type": row["document_type"],
                        "chunk_number": row["chunk_number"],
                    },
                    "source": row["document_name"],
                    "distance": 1 - row["similarity"],
                    "keyword_score": 1,
                }
            )

    return documents