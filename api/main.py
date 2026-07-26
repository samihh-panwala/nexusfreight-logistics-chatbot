print("1")
from fastapi import FastAPI, HTTPException
print("2")
from fastapi.middleware.cors import CORSMiddleware
print("3")
from pydantic import BaseModel
print("4")
from database_query import get_all_shipments_with_delivery
print("5")
from database.risk_engine import build_risk_report
print("6")
import uuid
print("7")
from chatbot import chat
print("8")
from rag.retriever import get_shipment
print("9")
from typing import List
print("10")
from pydantic import BaseModel
import traceback

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
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
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

@app.get("/risk-report")
def risk_report():

    shipments = get_all_shipments_with_delivery()

    report = build_risk_report(shipments)

    return report