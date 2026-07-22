# NexusFreight AI - Prompt Engineering Guide

## Overview

The NexusFreight AI chatbot relies on a carefully designed system prompt to ensure accurate, grounded, and domain-specific responses. The prompt instructs the Large Language Model (LLM) to behave as an internal logistics assistant rather than a general-purpose chatbot.

The objective is to minimize hallucinations while ensuring responses remain useful, professional, and based on verified company information.

---

# Role Definition

The chatbot is instructed to act as:

> **NexusFreight Internal Logistics AI Assistant**

This role ensures the model focuses only on logistics-related tasks including:

- Shipment tracking
- Delivery information
- Warehouse operations
- Carrier information
- Customs documentation
- Risk analysis
- Internal logistics documentation

The assistant is not intended to answer unrelated general knowledge questions.

---

# Domain Restrictions

The system prompt limits responses to NexusFreight business knowledge.

Supported topics include:

- Shipments
- Booking information
- Warehouses
- Products
- Vehicles
- Routes
- Carriers
- Customs
- Weather impact
- Delivery history
- Logistics documentation
- Shipment risk reports

If information is unavailable, the chatbot politely informs the user instead of generating fabricated information.

---

# Grounding Rules

One of the most important prompt instructions is:

> Never invent logistics data.

The chatbot must always use retrieved information.

Possible sources include:

- PostgreSQL / Supabase
- ChromaDB
- Hybrid Retrieval

The LLM is instructed to generate responses only after retrieval is completed.

This greatly reduces hallucination.

---

# SQL Data Handling

When structured information is required, the prompt instructs the assistant to rely on PostgreSQL data.

Examples:

- Shipment status
- Booking information
- Customer details
- Vehicle records
- Warehouse information
- Delivery history

The chatbot presents SQL results in a natural language format.

---

# ChromaDB Knowledge Handling

When documentation-based questions are received, the assistant uses ChromaDB.

Examples:

- Incoterms
- Customs procedures
- Company policies
- Logistics workflow
- Warehousing guide

Only retrieved document chunks are used while answering.

---

# Hybrid Retrieval

Some questions require both:

- Structured data
- Company knowledge

Example:

> Why is shipment SHP2045 delayed?

The chatbot retrieves:

From PostgreSQL

- Shipment status
- Delay days
- Route
- Warehouse

From ChromaDB

- Delay causes
- Operational guidelines
- Risk documentation

The LLM combines both contexts into a single response.

---

# Risk Instructions

Whenever shipment risk is involved, the prompt encourages the model to include:

- Risk Level
- Delay Information
- Reason
- Recommended Action

Example:

Risk Level:
HIGH

Reason:
Shipment delayed by 6 days due to customs clearance.

Recommended Action:
Contact customs broker and notify customer.

---

# Conversation Memory

The prompt allows the assistant to use previous conversation history.

Example:

User:
Show SHP2045

User:
What is its delay?

The assistant understands "its" refers to SHP2045 without asking again.

---

# Response Style

Responses are instructed to be:

- Professional
- Concise
- Easy to understand
- Business appropriate

Large SQL outputs are summarized whenever possible.

---

# Hallucination Prevention

The prompt contains multiple safeguards.

The assistant is instructed to:

- Never guess shipment information
- Never create fake booking IDs
- Never fabricate customer records
- Never invent delivery dates
- Never produce unsupported statistics

If no information exists, it clearly informs the user.

---

# Prompt Evolution During Development

Several improvements were made during development.

## Problem 1

Issue:

The LLM generated shipment information that did not exist.

Solution:

Added strict grounding rules.

Result:

Responses now depend on retrieved database context.

---

## Problem 2

Issue:

Shipment responses ignored risk level.

Solution:

Prompt updated to always include risk information.

Result:

Risk-aware responses became consistent.

---

## Problem 3

Issue:

Follow-up questions lost previous context.

Solution:

Conversation history included with every request.

Result:

Multi-turn conversations improved significantly.

---

## Problem 4

Issue:

Document answers were too generic.

Solution:

Restricted answers to retrieved ChromaDB context.

Result:

Higher factual accuracy.

---

## Problem 5

Issue:

Responses were too lengthy.

Solution:

Prompt instructed the model to summarize where appropriate.

Result:

Cleaner business-friendly answers.

---

# Prompt Flow

User Question

↓

Conversation History

↓

Query Router

↓

Retrieve Context

↓

Insert System Prompt

↓

Generate Final Prompt

↓

LLM API

↓

AI Response

---

# Benefits of Prompt Engineering

The final prompt provides:

- Reduced hallucination
- Better SQL grounding
- Better document understanding
- Consistent shipment responses
- Better follow-up conversations
- Improved risk explanations
- Professional business communication
