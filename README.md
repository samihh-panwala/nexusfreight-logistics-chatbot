# 🚚 NexusFreight AI

## Enterprise Logistics Intelligence Platform

NexusFreight AI is an enterprise-grade internal logistics assistant developed to help logistics teams retrieve shipment information, analyze delivery risks, access organizational knowledge, and answer operational questions through a conversational AI interface.

The system combines **Large Language Models (LLMs)**, **Hybrid Retrieval-Augmented Generation (Hybrid RAG)**, **PostgreSQL/Supabase**, and **ChromaDB** to provide intelligent responses using both structured logistics data and unstructured company documentation.

Unlike a traditional chatbot, NexusFreight AI understands logistics operations, shipment workflows, warehouse management, customs procedures, transportation routes, delivery history, and shipment risk analysis. It retrieves real company information before generating responses, reducing hallucinations while improving answer accuracy.

---

# 📌 Project Overview

The NexusFreight AI platform was designed as an internal enterprise assistant for logistics organizations where employees frequently need access to shipment information, operational documents, warehouse records, customer information, and shipment risk insights.

Instead of manually searching multiple databases or documentation, employees can simply ask questions in natural language. The chatbot automatically determines whether the answer should come from:

- Structured database records
- Internal logistics documentation
- Or a combination of both

The platform also includes an interactive **Risk Dashboard** that visualizes shipment delays, delivery performance, transportation trends, and AI-generated shipment risk classifications.

---

# 🎯 Business Problem

Large logistics organizations store information in multiple systems:

- Shipment databases
- Warehouse records
- Customer information
- Delivery history
- Operational manuals
- Logistics policies
- Customs documentation
- Incoterms reference documents

Finding information often requires employees to manually search across multiple applications, resulting in increased response time and operational inefficiency.

NexusFreight AI addresses this challenge by providing a single conversational interface capable of retrieving information from both structured and unstructured enterprise knowledge sources.

---

# 👥 Intended Users

The chatbot is designed for internal logistics personnel including:

- Logistics Coordinators
- Warehouse Managers
- Operations Managers
- Customer Support Executives
- Dispatch Teams
- Supply Chain Analysts
- Delivery Coordinators
- Business Operations Teams

---

# ✨ Key Features

### 🤖 AI Conversational Assistant

- Natural language interaction
- Multi-turn conversation support
- Context-aware responses
- Conversation memory

---

### 📦 Shipment Information Retrieval

Retrieve shipment details using Shipment ID or Booking ID, including:

- Shipment Status
- Shipment Type
- Delivery Status
- Shipping Mode
- Priority
- Delay Information
- Risk Level
- Recommended Actions

---

### 📚 Knowledge Base Search

The chatbot searches enterprise documentation using semantic similarity through ChromaDB.

Supported knowledge includes:

- Incoterms
- Customs Procedures
- Logistics Policies
- Warehouse Operations
- Shipment Guidelines
- Company Documentation
- Operational Manuals

---

### 🗄 Structured Database Search

Retrieve information directly from PostgreSQL/Supabase including:

- Customers
- Warehouses
- Shipments
- Routes
- Vehicles
- Products
- Weather
- Carriers
- Delivery History
- AI Monitoring Data

---

### 🔀 Hybrid Retrieval

When a question requires both structured records and document knowledge, the chatbot automatically combines both retrieval methods before generating the final AI response.

---

### 📊 Risk Dashboard

The Streamlit dashboard provides interactive analytics including:

- Shipment Risk Distribution
- Delivery Performance
- Delay Analysis
- Shipping Mode Statistics
- Priority Analysis
- Top Delayed Shipments
- Shipment Search & Filtering
- CSV Report Export

---

### ⚡ FastAPI Backend

REST API endpoints support:

- AI Chat
- Shipment Retrieval
- Risk Dashboard Analytics

making the backend reusable for additional enterprise applications.

---

# ⚙️ Installation Guide

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/nexusfreight-ai.git
cd nexusfreight-ai
```

---

## 2. Create a Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a file named:

```
.env
```

using the template provided in:

```
.env.example
```

Example:

```env
SUPABASE_URL=
SUPABASE_KEY=
GROQ_API_KEY=
GOOGLE_API_KEY=
OPENROUTER_API_KEY=
```

> Never commit the `.env` file or API keys to GitHub.

---

## 5. Configure the Database

The project uses **Supabase PostgreSQL** as the structured database.

Ensure that:

- Database is online
- Required tables are available
- Credentials are correctly configured inside `.env`

---

## 6. Verify ChromaDB

The chatbot uses ChromaDB for semantic document retrieval.

Verify that:

- Documents have been processed
- Embeddings are created
- Chroma database exists

Example structure:

```
chroma_db/
```

If required, regenerate the embeddings:

```bash
python rag/chunk_documents.py
python rag/vector_store.py
```

---

# ▶ Running the Application

Open two separate terminals.

---

## Terminal 1 – Start FastAPI

```bash
uvicorn api.main:app --reload
```

Default URL

```
http://127.0.0.1:8000
```

---

## Terminal 2 – Start Streamlit

```bash
streamlit run streamlit_app.py
```

Default URL

```
http://localhost:8501
```

---

# ✔ Startup Sequence

```
Clone Repository
        │
        ▼
Create Virtual Environment
        │
        ▼
Install Requirements
        │
        ▼
Configure .env
        │
        ▼
Connect Supabase
        │
        ▼
Verify ChromaDB
        │
        ▼
Start FastAPI
        │
        ▼
Start Streamlit
        │
        ▼
Open Chatbot
        │
        ▼
Ask Questions
```

---

# 📂 Project Structure

```
nexusfreight_ai/
│
├── api/
│   └── main.py
│
├── database/
│   ├── risk_engine.py
│   └── supabase_config.py
│
├── providers/
│   ├── gemini_provider.py
│   ├── groq_provider.py
│   └── openrouter_provider.py
│
├── rag/
│   ├── retriever.py
│   ├── search.py
│   ├── vector_store.py
│   ├── vector_store_excel.py
│   └── chunk_documents.py
│
├── datasets/
│
├── documents/
│
├── pages/
│   └── 2_Risk_Dashboard.py
│
├── streamlit_app.py
├── chatbot.py
├── llm_manager.py
├── hybrid_router.py
├── database_router.py
├── query_router.py
├── sql_engine.py
├── memory.py
├── prompt_builder.py
├── system_prompt.py
├── table_config.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📌 Major Components

| Component | Responsibility |
|-----------|----------------|
| Streamlit | User Interface |
| FastAPI | REST API Backend |
| Query Router | Determines SQL / Vector / Hybrid route |
| PostgreSQL | Structured logistics data |
| ChromaDB | Semantic knowledge retrieval |
| LLM Manager | Handles AI provider communication |
| Memory | Multi-turn conversation context |
| Risk Engine | Shipment risk prediction |
| Dashboard | Risk analytics visualization |

---