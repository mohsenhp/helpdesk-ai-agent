# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-07-14

### Added

- LangGraph-based enterprise help-desk agent
- SQL, vector, and hybrid retrieval routes
- Gemini-based routing, retrieval planning, question resolution, and answer synthesis
- SQLite-backed structured help-desk data
- Chroma-based semantic document retrieval
- Local Hugging Face embeddings
- Context-aware follow-up questions
- PostgreSQL-backed LangGraph checkpoint persistence
- Interactive CLI
- FastAPI REST API
- Docker and Docker Compose support
- Unit and integration test suites
- Conversational-memory integration tests
- GitHub Actions CI
- Docker container smoke testing

### Architecture

- SQLite stores structured fictional enterprise data
- Chroma stores vector embeddings
- PostgreSQL stores LangGraph checkpoints
- Gemini handles reasoning and response generation
- FastAPI exposes the agent over HTTP
