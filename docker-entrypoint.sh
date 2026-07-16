#!/bin/sh

set -e

if [ "${INITIALIZE_LOCAL_DATA:-false}" = "true" ] && [ ! -f "/app/runtime/helpdesk.db" ]; then
    echo "Initializing help-desk database..."
    python -m app.database.initialize
else
    echo "Skipping local database initialization."
fi

if [ "${INITIALIZE_LOCAL_DATA:-false}" = "true" ] && [ ! -f "/app/runtime/chroma/chroma.sqlite3" ]; then
    echo "Building Chroma vector database..."
    python -m app.vector.loader
else
    echo "Skipping local vector database initialization."
fi

echo "Initializing LangGraph checkpoint storage..."
python -m app.agent.checkpoint

echo "Starting HelpDesk AI Agent API..."

exec uvicorn app.api.application:app \
    --host 0.0.0.0 \
    --port 8000
