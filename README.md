# 🚚 NexusFreight AI Logistics Assistant

An AI-powered enterprise logistics assistant that combines **PostgreSQL**, **Supabase**, **ChromaDB**, and **Large Language Models (LLMs)** to provide intelligent shipment tracking, logistics insights, and risk analysis through a modern Streamlit interface.

---

# 📌 Features

- 🤖 AI-powered Logistics Chatbot
- 📦 Shipment Tracking
- 🚚 Warehouse & Vehicle Information
- 📊 Interactive Risk Dashboard
- 🔍 Hybrid Retrieval (SQL + Vector Search)
- 📚 Document Question Answering
- ⚡ FastAPI Backend
- 🎨 Modern Streamlit UI
- 📈 Shipment Risk Analytics
- 🌍 Incoterms & Logistics Knowledge Base
- 💾 Supabase Integration
- 🧠 ChromaDB Vector Search
- 🔄 Context-aware AI Conversations

---

# 🏗 Project Architecture

```
                User
                  │
                  ▼
          Streamlit Frontend
                  │
                  ▼
            FastAPI Backend
                  │
     ┌────────────┴────────────┐
     │                         │
     ▼                         ▼
 PostgreSQL / Supabase      ChromaDB
     │                         │
     └────────────┬────────────┘
                  ▼
            Prompt Builder
                  ▼
             LLM Provider
        (Groq / Gemini / OpenRouter)
                  ▼
             AI Response
```

---

# 📂 Project Structure

```
NexusFreight-AI
│
├── api/
├── database/
├── datasets/
├── documents/
├── embeddings/
├── pages/
├── providers/
├── rag/
│
├── chatbot.py
├── streamlit_app.py
├── llm_manager.py
├── query_router.py
├── sql_engine.py
├── prompt_builder.py
├── memory.py
├── shipment_details.py
├── database_query.py
├── hybrid_router.py
├── system_prompt.py
├── table_config.py
├── requirements.txt
└── README.md
```

---

# 🛠 Technologies Used

### Frontend

- Streamlit
- Plotly

### Backend

- FastAPI
- Uvicorn

### Database

- PostgreSQL
- Supabase

### AI

- Groq API
- Google Gemini
- OpenRouter

### Vector Database

- ChromaDB
- Sentence Transformers

### Data Processing

- Pandas
- OpenPyXL
- PyMuPDF

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/NexusFreight-AI.git

cd NexusFreight-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙ Configuration

Create a `config.py` file (or `.env`) containing your API credentials.

Example:

```python
GROQ_API_KEY = "YOUR_API_KEY"

SUPABASE_URL = "YOUR_SUPABASE_URL"

SUPABASE_KEY = "YOUR_SUPABASE_KEY"
```

**Do not commit your actual API keys to GitHub.**

---

# ▶ Running FastAPI

```bash
uvicorn api.main:app --reload
```

Backend will start at

```
http://127.0.0.1:8000
```

---

# ▶ Running Streamlit

```bash
streamlit run streamlit_app.py
```

---

# 📊 Dashboard Features

- Shipment Risk Distribution
- Delay Analytics
- Shipping Mode Analysis
- Priority Analysis
- Delivery Status
- Search & Filtering
- CSV Report Export

---

# 💬 AI Assistant Capabilities

The chatbot can answer questions about:

- Shipments
- Customers
- Warehouses
- Products
- Routes
- Vehicles
- Carriers
- Weather
- Customs
- Delivery History
- Incoterms
- Logistics Documentation
- Risk Prediction
- Shipment Delays

---

# 📚 Knowledge Base

The AI uses a hybrid knowledge base consisting of:

- Structured PostgreSQL Data
- Supabase Tables
- Logistics PDF Documents
- CSV Datasets
- ChromaDB Vector Embeddings

---

# 🚀 Future Enhancements

- Voice Assistant
- Real-time Shipment Tracking
- Interactive Maps
- Predictive ETA
- Automated Email Alerts
- Advanced Analytics
- Multi-language Support

---

# 👨‍💻 Developed By

**Samih Panwala**

Computer Engineering Student

AI & Data Science Enthusiast

---

# 📄 License

This project is developed for educational and internship purposes.