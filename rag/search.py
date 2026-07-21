import chromadb
import re
from sentence_transformers import SentenceTransformer

# -------------------------------------------------
# Embedding Model
# -------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------------------------
# ChromaDB
# -------------------------------------------------

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="logistics_documents"
)

# -------------------------------------------------
# Document Routing Keywords
# -------------------------------------------------

DOCUMENT_FILTERS = {

    "incoterm": [
        "incoterm",
        "incoterms"
    ],

    "customs": [
        "custom",
        "customs",
        "clearance",
        "import",
        "export"
    ],

    "warehouse": [
        "warehouse",
        "warehouses",
        "storage",
        "inventory"
    ],

    "shipment": [
        "shipment",
        "shipments",
        "tracking",
        "delivery",
        "booking"
    ],

    "carrier": [
        "carrier",
        "carriers",
        "transport",
        "shipping company"
    ],

    "customer": [
        "customer",
        "customers",
        "client"
    ],

    "vehicle": [
        "vehicle",
        "vehicles",
        "truck"
    ],

    "route": [
        "route",
        "routes",
        "path"
    ],

    "weather": [
        "weather",
        "storm",
        "rain",
        "temperature"
    ],

    "ai": [
        "ai",
        "prediction",
        "risk",
        "delay",
        "model",
        "monitoring",
        "feature"
    ]
}

# -------------------------------------------------
# Detect Best Matching Document
# -------------------------------------------------

def detect_document(query):

    query = query.lower()

    for document, keywords in DOCUMENT_FILTERS.items():

        for keyword in keywords:

            if keyword in query:

                return document

    return None


# -------------------------------------------------
# Map Document Key to Actual File Name
# -------------------------------------------------

DOCUMENT_FILES = {

    "incoterm":
        "Incoterms International Trade Terms Guide.txt",

    "customs":
        "Customs.txt",

    "warehouse":
        "Warehouses.txt",

    "shipment":
        "Shipments.txt",

    "carrier":
        "Carriers.txt",

    "customer":
        "Customers.txt",

    "vehicle":
        "Vehicles.txt",

    "route":
        "Routes.txt",

    "weather":
        "Weather.txt",

    "ai":
        "AI_Inference_Log.txt"
}

# -------------------------------------------------
# Remember Last Document
# -------------------------------------------------

LAST_DOCUMENT = None

# -------------------------------------------------
# Keyword Score
# -------------------------------------------------

def keyword_score(query, text):

    query_words = set(
        re.findall(r"\w+", query.lower())
    )

    text_words = set(
        re.findall(r"\w+", text.lower())
    )

    return len(query_words & text_words)


def search_documents(query, top_k=6):

    global LAST_DOCUMENT

    document_key = detect_document(query)

    query_lower = query.lower()

    # -------------------------------------------------
    # Only filter for definition-type questions
    # -------------------------------------------------

    definition_words = [
        "what is",
        "define",
        "definition",
        "meaning",
        "explain"
    ]

    use_filter = False

    if document_key:

        LAST_DOCUMENT = document_key

        if any(word in query_lower for word in definition_words):

            use_filter = True

    elif LAST_DOCUMENT and any(word in query_lower for word in definition_words):

        document_key = LAST_DOCUMENT
        use_filter = True

    where_filter = None

    if use_filter:

        filename = DOCUMENT_FILES.get(document_key)

        if filename:

            where_filter = {
                "document_name": filename
            }

    # -------------------------------------------------
    # Query ChromaDB
    # -------------------------------------------------

    try:

        if where_filter:

            results = collection.query(
                query_texts=[query],
                where=where_filter,
                n_results=top_k,
                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]
            )

        else:

            results = collection.query(
                query_texts=[query],
                n_results=top_k,
                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]
            )

    except Exception as e:

        print("Search Error:", e)

        return []

    if not results["documents"]:

        return []

    documents = []

    print("\n========== CHROMADB RESULTS ==========")

    for i in range(len(results["documents"][0])):

        metadata = results["metadatas"][0][i]

        distance = results["distances"][0][i]

        print(
            metadata.get("document_name", "Unknown"),
            "Distance:",
            round(distance, 4)
        )

        text = results["documents"][0][i]

        documents.append({

            "chunk_id": results["ids"][0][i],

            "document": text,

            "metadata": metadata,

            "source": metadata.get("document_name", "Unknown"),

            "distance": distance,

            "keyword_score": keyword_score(query, text)

        })

    print("======================================\n")

    # -------------------------------------------------
    # Re-rank
    # -------------------------------------------------

    documents = sorted(

        documents,

        key=lambda x: (
            -x["keyword_score"],
            x["distance"]
        )

    )

    # -------------------------------------------------
    # Keep only reasonably relevant chunks
    # -------------------------------------------------

    filtered = []

    for doc in documents:

        if len(filtered) >= 4:
            break

        if doc["distance"] <= 1.8:
            filtered.append(doc)

    if not filtered:
        filtered = documents[:4]

    return filtered 