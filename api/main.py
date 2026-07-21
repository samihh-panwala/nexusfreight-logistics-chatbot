from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database_query import get_all_shipments_with_delivery
from database.risk_engine import build_risk_report

import uuid
import chromadb
from sentence_transformers import SentenceTransformer

from chatbot import chat
from rag.retriever import get_shipment
from typing import List
from pydantic import BaseModel

# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(
    title="NexusFreight Logistics AI API",
    description="Backend API for NexusFreight Logistics AI Chatbot",
    version="1.0"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Constants
# =====================================================

CHUNK_SIZE = 250
COLLECTION_NAME = "logistics_documents"

CUSTOMER_FILTERS = {

    "customer_status": {

        "active": "Active",

        "inactive": "Inactive"

    },

    "customer_type": {

        "business": "Business",

        "individual": "Individual"

    }

}


PRODUCT_FILTERS = {

    "hazardous": {

        "hazardous": True

    },

    "fragile": {

        "fragile": True

    },

    "perishable": {

        "perishable": True

    }

}


SHIPMENT_FILTERS = {

    "priority": {

        "high priority": "High",

        "normal": "Normal",

        "low priority": "Low"

    }

}

# =====================================================
# Models
# =====================================================
'''
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)
'''

# =====================================================
# Request Model
# =====================================================

class ChatRequest(BaseModel):
    message: str

# =====================================================
# Home
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to NexusFreight Logistics AI API",
        "status": "Running"
    }

# =====================================================
# Chat Endpoint
# =====================================================

@app.post("/chat")
def chatbot_api(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        result = chat(request.message)

        return {
            "user_message": request.message,
            "bot_response": result["answer"],
            "query_type": result["query_type"],
            "source": result["source"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chatbot Error: {str(e)}"
        )

# =====================================================
# Shipment Endpoint
# =====================================================

@app.get("/shipment/{shipment_id}")
def shipment_api(shipment_id: str):

    try:

        shipment = get_shipment(shipment_id)

        if shipment is None:

            raise HTTPException(
                status_code=404,
                detail="Shipment not found."
            )

        return shipment

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================================
# Upload Document
# =====================================================

@app.post("/upload-doc")
async def upload_document(file: UploadFile = File(...)):
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    try:

        # -----------------------------
        # Validate File
        # -----------------------------

        if not file.filename.endswith(".txt"):

            raise HTTPException(
                status_code=400,
                detail="Only .txt files are allowed."
            )

        # -----------------------------
        # Read File
        # -----------------------------

        content = (await file.read()).decode("utf-8")

        words = content.split()

        chunks = [

            " ".join(words[i:i + CHUNK_SIZE])

            for i in range(0, len(words), CHUNK_SIZE)

        ]

        chunks = [

            chunk

            for chunk in chunks

            if chunk.strip()

        ]

        if len(chunks) == 0:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # -----------------------------
        # Generate Embeddings
        # -----------------------------

        embeddings = embedding_model.encode(
            chunks,
            normalize_embeddings=True
        ).tolist()

        # -----------------------------
        # Store in ChromaDB
        # -----------------------------

        for i, chunk in enumerate(chunks):

            collection.add(

                ids=[str(uuid.uuid4())],

                documents=[chunk],

                embeddings=[embeddings[i]],

                metadatas=[

                    {

                        "document_name": file.filename,

                        "chunk": i + 1,

                        "document_type": "uploaded_document"

                    }

                ]

            )

        return {

            "message": "Document uploaded successfully.",

            "filename": file.filename,

            "chunks_created": len(chunks)

        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )



@app.get("/risk-report")
def risk_report():

    shipments = get_all_shipments_with_delivery()

    report = build_risk_report(shipments)

    return report