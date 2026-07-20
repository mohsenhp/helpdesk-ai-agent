# Helpdesk AI Agent 🤖💼

An AI-powered IT support assistant that combines structured SQL data with semantic knowledge retrieval to answer helpdesk questions using a Retrieval-Augmented Generation (RAG) architecture.

The application is built with **Python**, **LangGraph**, **FastAPI**, **Azure AI Search**, and **Google Gemini**, and is automatically deployed to **Azure Container Apps** through **GitHub Actions**.

---

## 🌐 Live Demo

The application is available at:

**https://helpdesk-ai-agent.kindmoss-7afefc50.northeurope.azurecontainerapps.io/**

---

## 🚀 Features

- 🤖 AI-powered IT support assistant
- 🔍 Hybrid search
  - Structured queries against SQL
  - Semantic search using Azure AI Search
- 📚 Retrieval-Augmented Generation (RAG)
- 🧠 LangGraph agent workflow
- 🌐 REST API with FastAPI
- ☁️ Azure-native deployment
- 🐳 Docker containerized
- 🔄 Automated CI/CD with GitHub Actions

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| AI | LangChain, LangGraph, Google Gemini |
| Vector Search | Azure AI Search |
| Database | Azure SQL, SQLite |
| API | FastAPI |
| Language | Python |
| Containerization | Docker |
| Cloud | Azure Container Apps |
| CI/CD | GitHub Actions |

---

## 🏗️ Architecture

```text
                User
                  │
                  ▼
             FastAPI API
                  │
                  ▼
            LangGraph Agent
           ┌────────┴────────┐
           ▼                 ▼
     Azure SQL         Azure AI Search
           │                 │
           └────────┬────────┘
                    ▼
               Google Gemini
                    │
                    ▼
                 Response
```

---

## 📁 Project Structure

```text
app/
├── agent/
├── api/
├── config/
├── database/
├── providers/
├── tools/
└── vector/

tests/

.github/workflows/
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Docker (optional)
- Azure CLI (for deployment)

### Clone the repository

```bash
git clone https://github.com/mohsenhp/helpdesk-ai-agent.git
cd helpdesk-ai-agent
```

### Create a virtual environment

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment

Create a `.env` file from `.env.example`.

Example settings:

```env
GOOGLE_API_KEY=

DATABASE_PROVIDER=sqlite

VECTOR_STORE_PROVIDER=azure

AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=
AZURE_SEARCH_INDEX=

AZURE_SQL_CONNECTION_STRING=
```

---

## ▶️ Running the application

```bash
python -m app.main
```

or

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Running tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## ☁️ Azure Deployment

The project is automatically deployed using GitHub Actions.

Deployment pipeline:

1. Run the test suite
2. Build the Docker image
3. Push the image to Azure Container Registry
4. Deploy to Azure Container Apps
5. Configure Azure AI Search and Azure SQL environment variables

---



## 🔄 Continuous Integration & Deployment

Every push to the `main` branch:

- ✅ Runs all tests
- ✅ Builds the Docker image
- ✅ Pushes the image to Azure Container Registry
- ✅ Deploys the latest version to Azure Container Apps

---

## 📄 License

This project is licensed under the MIT License.
