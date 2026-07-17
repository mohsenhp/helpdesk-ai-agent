# Azure Container Apps Deployment

This directory contains the deployment configuration for running the Helpdesk AI Agent on Azure Container Apps.

## Architecture

The production deployment uses the following Azure services:

- Azure Container Apps
- Azure Container Registry (ACR)
- Azure AI Search
- Azure SQL Database
- Azure OpenAI or Google Gemini
- PostgreSQL (LangGraph checkpoints, optional)

## Files

| File | Purpose |
|------|---------|
| `container-app.yaml` | Azure Container Apps deployment manifest |
| `environment.example` | Example production environment variables |
| `README.md` | Deployment documentation |

## Prerequisites

Create the following Azure resources before deployment:

- Azure Container Registry
- Azure Container Apps Environment
- Azure Container App
- Azure AI Search
- Azure SQL Database

Optional:

- Azure OpenAI
- Azure Database for PostgreSQL (LangGraph checkpoints)

## Build the Docker image

```bash
docker build -t helpdesk-ai-agent .
```

## Push the image

```bash
docker tag helpdesk-ai-agent <registry>/helpdesk-ai-agent:latest
docker push <registry>/helpdesk-ai-agent:latest
```

Replace `<registry>` with your Azure Container Registry.

## Configure environment variables

Use `environment.example` as a reference when configuring environment variables and secrets in Azure Container Apps.

At minimum configure:

- `ENVIRONMENT`
- `DATABASE_PROVIDER`
- `VECTOR_STORE_PROVIDER`
- `LLM_PROVIDER`
- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_API_KEY`
- `AZURE_SEARCH_INDEX`
- `AZURE_SQL_CONNECTION_STRING`

Depending on the selected LLM provider:

### Google Gemini

- `GOOGLE_API_KEY`

### Azure OpenAI

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT`
- `AZURE_OPENAI_API_VERSION`

## Deploy

Deploy using:

- Azure Portal
- Azure CLI
- GitHub Actions
- Azure DevOps

The application listens on port **8000**.

## Notes

- Do not commit production secrets.
- Store secrets using Azure Container Apps secrets or Azure Key Vault.
- Set `INITIALIZE_LOCAL_DATA=false` in production.
- Use Azure AI Search as the production vector store.
