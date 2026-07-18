# Azure Container Apps Deployment

This directory contains the deployment documentation and configuration for running the HelpDesk AI Agent on Azure Container Apps.

## Architecture

The production deployment uses:

* Azure Container Apps
* Azure Container Registry (ACR)
* Azure AI Search
* Azure SQL Database
* Google Gemini (LLM provider)
* PostgreSQL (optional LangGraph checkpoint storage)

Production flow:

```
Client
  |
  v
Azure Container Apps
  |
  v
FastAPI API
  |
  v
LangGraph Agent
  |
  +--> Azure SQL Database
  |
  +--> Azure AI Search
  |
  +--> Google Gemini
```

---

## Prerequisites

Create the following Azure resources:

* Azure Container Registry
* Azure Container Apps Environment
* Azure Container App
* Azure AI Search service
* Azure SQL Database

Optional:

* Azure Database for PostgreSQL (LangGraph checkpoint storage)
* Azure OpenAI Service

---

# Build the Docker image

Build locally:

```bash
docker build -t helpdesk-ai-agent .
```

Or build directly in Azure Container Registry:

```bash
az acr build \
  --registry <registry-name> \
  --image helpdesk-ai-agent:latest .
```

---

# Push the image

Tag the image:

```bash
docker tag helpdesk-ai-agent \
  <registry>.azurecr.io/helpdesk-ai-agent:latest
```

Push:

```bash
docker push \
  <registry>.azurecr.io/helpdesk-ai-agent:latest
```

Example:

```bash
docker tag helpdesk-ai-agent \
  helpdeskaiagentacr.azurecr.io/helpdesk-ai-agent:latest

docker push \
  helpdeskaiagentacr.azurecr.io/helpdesk-ai-agent:latest
```

---

# Configure environment variables

Configure the following variables in Azure Container Apps.

Required:

| Variable | Description |
|---|---|
| `ENVIRONMENT` | Application environment |
| `DATABASE_PROVIDER` | Database backend |
| `VECTOR_STORE_PROVIDER` | Vector database backend |
| `LLM_PROVIDER` | LLM provider |
| `AZURE_SEARCH_ENDPOINT` | Azure AI Search endpoint |
| `AZURE_SEARCH_API_KEY` | Azure AI Search key |
| `AZURE_SEARCH_INDEX` | Search index name |
| `AZURE_SQL_CONNECTION_STRING` | SQL Database connection string |

Production example:

```text
ENVIRONMENT=production
DATABASE_PROVIDER=azure
VECTOR_STORE_PROVIDER=azure
INITIALIZE_LOCAL_DATA=false
```

---

# LLM Configuration

## Google Gemini

Required:

```text
GOOGLE_API_KEY
```

Optional:

```text
GEMINI_MODEL
```

Example:

```text
GEMINI_MODEL=gemini-3.5-flash
```

---

## Azure OpenAI

Required:

```text
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
AZURE_OPENAI_API_VERSION
```

---

# Migrate documents to Azure AI Search

After configuring Azure AI Search:

```bash
python -m app.vector.migrate
```

This uploads knowledge base documents from the local dataset into Azure AI Search.

Production should use:

```text
VECTOR_STORE_PROVIDER=azure
```

and:

```text
INITIALIZE_LOCAL_DATA=false
```

---

# Deploy the Container App

Update the application image:

```bash
az containerapp update \
  --name helpdesk-ai-agent \
  --resource-group <resource-group> \
  --image <registry>.azurecr.io/helpdesk-ai-agent:latest
```

Azure Container Apps creates a new revision automatically.

Check revisions:

```bash
az containerapp revision list \
  --name helpdesk-ai-agent \
  --resource-group <resource-group> \
  -o table
```

Example output:

```text
Name                         HealthState
---------------------------  ----------
helpdesk-ai-agent--revision1 Healthy
```

---

# Route traffic to a revision

Send 100% traffic to a revision:

```bash
az containerapp ingress traffic set \
  --name helpdesk-ai-agent \
  --resource-group <resource-group> \
  --revision-weight <revision-name>=100
```

Example:

```bash
az containerapp ingress traffic set \
  --name helpdesk-ai-agent \
  --resource-group rg-hadianpour-5629 \
  --revision-weight helpdesk-ai-agent--gemini-fix1=100
```

---

# Verify deployment

## Health check

```bash
curl https://<container-app-fqdn>/health
```

Expected:

```json
{
  "status": "ok",
  "environment": "production"
}
```

---

## Metadata endpoint

```bash
curl https://<container-app-fqdn>/metadata
```

Example:

```json
{
  "name": "HelpDesk AI Agent",
  "version": "0.1.0",
  "capabilities": [
    "ticket_search",
    "incident_analysis",
    "knowledge_base_search"
  ],
  "environment": "production"
}
```

---

## Test the AI agent

Example:

```bash
curl -X POST https://<container-app-fqdn>/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"How many open Critical VPN tickets are there?"}'
```

Expected:

```json
{
  "answer": "There are 2 open Critical VPN tickets.",
  "conversation_id": "..."
}
```

---

# Troubleshooting

## View application logs

```bash
az containerapp logs show \
  --name helpdesk-ai-agent \
  --resource-group <resource-group> \
  --revision <revision-name> \
  --type console
```

---

## Check environment variables

```bash
az containerapp exec \
  --name helpdesk-ai-agent \
  --resource-group <resource-group> \
  --revision <revision-name> \
  --command printenv
```

---

## Check active revisions

```bash
az containerapp revision list \
  --name helpdesk-ai-agent \
  --resource-group <resource-group> \
  -o table
```

---

# Secrets

Never commit production secrets.

Use:

* Azure Container Apps secrets
* Azure Key Vault

Example secret names:

```text
azure-sql-connection-string
google-api-key
azure-openai-api-key
```

---

# Production Notes

* Production uses Azure SQL Database.
* Production uses Azure AI Search.
* Local SQLite and Chroma initialization should be disabled.
* Keep `environment.example` updated when adding configuration values.
* Each deployment creates a new Container Apps revision.
* Test the new revision before moving 100% traffic.
* Remove unused revisions periodically.
