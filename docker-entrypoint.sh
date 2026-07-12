#!/bin/sh

set -e

if [ ! -f "/app/runtime/helpdesk.db" ]; then
    echo "SQLite database not found."
    echo "Initializing help-desk database..."

    python -m app.database.initialize
else
    echo "SQLite database already exists."
fi

if [ ! -f "/app/runtime/chroma/chroma.sqlite3" ]; then
    echo "Vector database not found."
    echo "Building Chroma vector database..."

    python -m app.vector.loader
else
    echo "Vector database already exists."
fi

echo "Starting HelpDesk AI Agent API..."

exec uvicorn app.api.application:app \
    --host 0.0.0.0 \
    --port 8000
