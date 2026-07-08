# NexusFreight Logistics AI Chatbot

## Overview

The NexusFreight Logistics AI Chatbot is a Retrieval-Augmented Generation (RAG) based chatbot developed to assist internal employees with logistics-related queries. The chatbot retrieves information from a Supabase knowledge base and uses the Groq Large Language Model (LLM) to generate accurate, context-aware responses.

---

## Features

- AI-powered logistics assistant
- Shipment status retrieval
- Shipment ID detection using Regex
- Order information retrieval
- Warehouse information lookup
- Tracking event retrieval
- FAQ support
- Groq LLM integration
- Supabase database integration
- Error handling
- Terminal-based chatbot

---

## Technologies Used

- Python 3.11
- Groq API
- Supabase
- PostgreSQL
- Regular Expressions (Regex)
- Retrieval-Augmented Generation (RAG)

---

## Project Structure

```
knowledge_base/
│
├── chatbot.py
├── config.py
├── system_prompt.py
│
├── datasets/
│   ├── shipments.csv
│   ├── orders.csv
│   ├── warehouses.csv
│   ├── delivery_agents.csv
│   ├── tracking_events.csv
│   └── faqs.csv
│
├── documents/
│
├── rag/
│   └── retriever.py
│
└── database/
```

---

## Workflow

User Query

↓

Shipment ID Detection (Regex)

↓

Retriever Module

↓

Supabase Database

↓

Retrieved Context

↓

Groq LLM

↓

Generated Response

---

## Sample Queries

```
What is the status of SHP0001?

Show latest 5 shipments

Show delivered shipments

Warehouse WH001

Track SHP0005

Show all delayed shipments

FAQ

What is customs clearance?
```

---

## Future Improvements

- Semantic Search
- Vector Embeddings
- FastAPI Integration
- Streamlit User Interface
- Conversational Memory
- Hybrid RAG
- Dashboard Integration

---

## Developer

**Panwala Mohammad Samih Sohel**

Computer Engineering Student

GTU

---

## Internship Project

AI Engineering Internship

NexusFreight Logistics AI Assistant