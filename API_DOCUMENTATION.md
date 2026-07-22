# NexusFreight AI API Documentation

## Overview

The NexusFreight AI backend is developed using **FastAPI** and exposes REST APIs that allow the Streamlit frontend to communicate with the chatbot, retrieve shipment information, and generate shipment risk analytics.

The APIs integrate with multiple backend services including:

- PostgreSQL / Supabase
- ChromaDB
- Hybrid Query Router
- Large Language Models (Groq / Gemini / OpenRouter)
- Shipment Risk Engine

Base URL

```
http://127.0.0.1:8000
```

---

# API List

| Endpoint | Method | Purpose |
|----------|--------|----------|
| `/chat` | POST | Process employee queries using Hybrid AI |
| `/shipment/{id}` | GET | Retrieve shipment details by Shipment ID |
| `/risk-report` | GET | Generate complete shipment risk analytics |

---

# 1. POST /chat

## Purpose

Processes an employee's logistics question and returns an AI-generated response.

This endpoint is responsible for:

- Understanding the user's query
- Maintaining conversation history
- Selecting the correct retrieval strategy
- Retrieving structured and/or unstructured information
- Generating the final AI response

---

## Request Format

```json
{
    "message": "Show shipment SHP0001",
    "history": [
        {
            "role": "user",
            "content": "Previous Question"
        }
    ]
}
```

---

## Processing Flow

```
User Question

↓

Conversation History

↓

Query Router

↓

SQL / VECTOR / HYBRID

↓

Retrieve Context

↓

Prompt Builder

↓

LLM API

↓

Final Response
```

---

## Successful Response

```json
{
    "bot_response":"Shipment SHP0001 has been delivered successfully.",
    "source":"PostgreSQL",
    "query_type":"SQL"
}
```

---

## Error Response

```json
{
    "detail":"Unable to process request."
}
```

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Invalid Request |
| 404 | Data Not Found |
| 500 | Internal Server Error |

---

# 2. GET /shipment/{id}

## Purpose

Retrieves complete shipment information using a Shipment ID.

The API searches the PostgreSQL/Supabase database and returns structured shipment information.

---

## Example Request

```
GET /shipment/SHP0001
```

---

## Successful Response

```json
{
    "shipment_id":"SHP0001",
    "booking_id":"BK0001",
    "shipment_type":"Export",
    "shipping_mode":"Air",
    "priority":"High",
    "delivery_status":"Delivered",
    "delay_days":2,
    "risk_level":"Low"
}
```

---

## Invalid Shipment Example

```json
{
    "detail":"Shipment not found."
}
```

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Shipment Retrieved |
| 404 | Shipment Not Found |
| 500 | Internal Server Error |

---

# 3. GET /risk-report

## Purpose

Generates shipment risk analytics used by the Streamlit Risk Dashboard.

The endpoint collects shipment data, performs risk calculations, and returns dashboard-ready information.

---

## Processing

```
Shipment Data

↓

Risk Engine

↓

Delay Analysis

↓

Risk Classification

↓

Summary Statistics

↓

Dashboard JSON
```

---

## Successful Response

```json
{
    "summary":{
        "total_shipments":250,
        "high_risk":12,
        "medium_risk":38,
        "low_risk":200
    },
    "all_shipments":[
        ...
    ]
}
```

---

## Risk Classification

The Risk Engine categorizes shipments into three levels:

### High Risk

- Large delivery delays
- Operational issues
- Customs blockage
- Route disruption

---

### Medium Risk

- Moderate delay
- Minor operational concern
- Requires monitoring

---

### Low Risk

- Normal shipment
- On-time delivery
- No operational concern

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Report Generated |
| 500 | Internal Server Error |

---

# Error Handling

The backend performs graceful error handling for:

- Database connection failures
- Missing shipment records
- Invalid requests
- ChromaDB retrieval failures
- LLM API failures
- API timeout errors

Users receive meaningful error messages instead of raw Python exceptions.

---

# Logging

The backend uses Python's `logging` module.

Typical logged events include:

- Chat request received
- Query routing decision
- Shipment retrieval
- Risk report generation
- ChromaDB retrieval
- LLM response generation
- API errors
- Database failures

Sensitive information such as API keys and credentials is never logged.

---

# API Workflow Summary

```
Streamlit UI

↓

FastAPI

↓

Conversation Memory

↓

Query Router

↓

PostgreSQL
OR
ChromaDB
OR
Hybrid Retrieval

↓

Prompt Builder

↓

LLM Provider

↓

AI Response

↓

Streamlit Frontend
```