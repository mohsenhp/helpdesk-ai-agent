#!/bin/sh

set -e

DATABASE_PROVIDER="${DATABASE_PROVIDER:-local}"
VECTOR_STORE_PROVIDER="${VECTOR_STORE_PROVIDER:-local}"

if [ "$DATABASE_PROVIDER" = "local" ] && \
   [ "${INITIALIZE_LOCAL_DATA:-false}" = "true" ] && \
   [ ! -f "/app/runtime/helpdesk.db" ]; then
    echo "Initializing local database..."
    python -m app.database.initialize
else
    echo "Skipping automatic database initialization."
fi

if [ "$VECTOR_STORE_PROVIDER" = "local" ] && \
   [ "${INITIALIZE_LOCAL_DATA:-false}" = "true" ] && \
   [ ! -f "/app/runtime/chroma/chroma.sqlite3" ]; then
    echo "Building local Chroma vector database..."
    python -m app.vector.loader
else
    echo "Skipping automatic vector-store initialization."
fi

echo "Initializing LangGraph checkpoint storage..."

python -m app.agent.checkpoint || {
    echo "Checkpoint initialization failed."
    exit 1
}

echo "Starting HelpDesk AI Agent API..."

exec uvicorn app.api.application:create_application \
    --factory \
    --host 0.0.0.0 \
    --port "${PORT:-8000}"
