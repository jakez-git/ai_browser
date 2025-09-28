# Local Chat UI with Live Knowledge Base

This repository hosts a locally runnable chat interface for an LLM, backed by a continuously updating knowledge base sourced from a watched directory tree.

## Quick Start

- Review governance docs in `docs/` for requirements, design vision, and testing standards.
- Follow the documented TDD workflow before implementing features.
- Use project documentation (e.g., `docs/ROADMAP.md`, `docs/backlog.md`) to track work and progress.

## Focus Areas

1. Build a chat UI capable of querying and conversing with a local LLM.
2. Implement a retrieval pipeline that indexes a root folder recursively and updates embeddings immediately when files change.
3. Support ingestion of transcripts, documents, and potentially videos (via automated transcription pipelines).
4. Explore alternative knowledge-integration strategies if they outperform traditional RAG for living documents.

## Repository Status

Project scaffolding is being established. See `docs/REQUIREMENTS.md` and `docs/ROADMAP.md` for prioritized backlog and next steps.
