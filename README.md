# Helpdesk AI Agent 🤖💼

An enterprise-grade, containerized AI assistant designed to automate IT support workflows, triage helpdesk tickets, and resolve internal queries. This project is built with cloud-native principles and is explicitly tailored for seamless hosting on **Azure Container Apps**.

---

## 🏗️ Architecture & Branching Strategy

The repository follows a progressive development pipeline aimed at modernizing legacy agent software into secure, scalable cloud infrastructure:

* **`main`**: Houses the stable core logic of the Helpdesk AI engine.
* **`cloud-foundation`**: Introduces containerization standards and agnostic cloud architecture patterns.
* **`azure-migration` (Active)**: Adapts the application to run natively on Azure infrastructure using Managed Identities, Azure OpenAI, and serverless containers.

---

## ⚙️ Configuration & Environment Matrix

The application utilizes targeted environment configurations depending on your deployment stage. **Never commit active `.env` files containing real secrets to the repository.**

| Environment File | Intended Target | Usage Key Elements |
| --- | --- | --- |
| `.env.example` | Local Machine Development | Direct LLM endpoints, local databases, debug logging. |
| `.env.production.example` | Hardened On-Prem/Standard VPS | High-performance configs, strict CORS, production telemetry. |
| `.env.azure.example` | Generic Azure Environments | Integrations with Azure App Services / VM scale groups. |
| `.env.azure.containerapp.example` | Azure Container Apps (ACA) | Managed Identity targets, Azure Key Vault secret injection. |

---

## 🚀 Getting Started

### Prerequisites

* Docker (Desktop or Engine)
* Azure CLI (If deploying to cloud)

### 1. Local Development Setup

Clone the repository and switch to the active migration branch:

git checkout azure-migration

Configure your local environment variables:

cp .env.example .env

*Open `.env` and fill out your local runtime configurations and API endpoints.*

### 2. Running via Docker

The application is pre-configured to build into a lightweight runtime container.

Build the local image:

docker build -t helpdesk-ai-agent:local .

Run the container locally:

docker run -d -p 8080:8080 --env-file .env helpdesk-ai-agent:local

---

## ☁️ Azure Container Apps Deployment

When moving to production on Azure, the environment relies heavily on configuration files designed for container environments.

1. **Prepare Secrets:** Copy the Container App configuration template:
cp .env.azure.containerapp.example .env.azure.containerapp
2. **Provision Infrastructure:** Use your Bicep, Terraform, or Azure CLI script to spin up an Azure Container Apps Environment and Link it to an Azure OpenAI service endpoint.
3. **Deploy Container:** Push the Docker image to an **Azure Container Registry (ACR)** and deploy directly into the serverless ACA infrastructure container pool.

---

## 🔒 Security & Git Hygiene

* **Exclusions:** The `.dockerignore` file ensures that heavy dependencies, testing cache, and local secret credentials are never embedded into production Docker images.
* **Secrets:** Ensure `.env` is present in your local `.gitignore` file to prevent accidental upstream pushes of private API keys.
