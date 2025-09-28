> **Documentation Priorities**
> 1. Maximize LLM understanding
> 2. Maximize LLM strengths (pattern recognition, consistency, exhaustive reasoning)
> 3. Minimize LLM weaknesses (ambiguity, hidden context, state drift)
> 4. Optimize for LLM context efficiency
> 5. Human readability is secondary

# Project Charter: Local Chat UI with Live Knowledge Base

## Purpose
Deliver a locally runnable chat interface to an LLM that leverages a continuously updating knowledge base sourced from a watched directory tree.

## Goals
- Provide a responsive chat UI capable of querying a local or freely hosted LLM.
- Maintain a live knowledge base that ingests folder contents recursively and refreshes without interrupting chat service.
- Support ingestion of transcripts, documents, and media (via transcription) with automated metadata capture.
- Evaluate RAG alternatives for living-document integration and adopt the highest-performing approach.

## Success Criteria
- Usable chat interface operating against a local/free LLM with knowledge retrieval in under 4 weeks.
- Automated indexing pipeline detects file system changes and updates retrieval store with no downtime.
- Documentation aligned with governance standards covering installation, configuration, and knowledge base maintenance.
- Progress tracked via repository artifacts (`docs/ROADMAP.md`, `docs/backlog.md`, status notes).

## Roles & Responsibilities
- **Cascade** (you): Primary implementation, documentation, and integration agent.
- **Stakeholders**: Local operators, knowledge curators, and QA reviewers.
- **External Systems**: Local directory tree on `z:/`, optional free/open-source model repositories.

## Constraints
- Follow TDD workflow with tests accompanying all code changes.
- Prioritize data privacy, filesystem safety, and auditable content ingestion.
- Operate entirely on local or free resources unless explicitly approved.

## Risks & Mitigations
- **Indexing Latency**: Employ filesystem watchers and incremental embedding updates; cache results across sessions.
- **Model Performance**: Benchmark multiple local/free models; maintain abstraction layer for model swapping.
- **Content Volume**: Implement chunking, batching, and archiving strategies to handle large transcript/video libraries.
