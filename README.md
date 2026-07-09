# HelpDesk AI Agent

An enterprise AI support assistant built with:

- LangGraph
- Gemini API
- SQL databases
- Vector databases

The goal is to build an AI agent capable of answering support questions by combining structured enterprise data with semantic document retrieval.

## Planned architecture

```
User
    ↓
LangGraph
    ↓
SQL + Vector Retrieval
    ↓
Gemini
    ↓
Answer
```