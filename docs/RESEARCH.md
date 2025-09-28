> **Documentation Priorities**
> 1. Maximize LLM understanding
> 2. Maximize LLM strengths (pattern recognition, consistency, exhaustive reasoning)
> 3. Minimize LLM weaknesses (ambiguity, hidden context, state drift)
> 4. Optimize for LLM context efficiency
> 5. Human readability is secondary

# Research Notes: Local LLM Chat with Live Knowledge Base

## Hardware Context
- CPU: Intel i9-12900 (16 cores, hybrid architecture)
- GPU: NVIDIA RTX 3060 (12 GB VRAM)
- RAM: 64 GB
- Storage: Tight `c:/` SSD, tight `d:/` HDD, ample network storage on `z:/` NAS (several TB) with slower access latency
- Docker Desktop with CUDA support available

## Candidate LLM Runtimes
- **llama.cpp**
  - Pros: Lightweight, supports GGUF quantized models, CPU+GPU hybrid, easy to embed in Python (via bindings) or run via server mode.
  - Cons: GPU acceleration limited to 8/16-bit; may require tuning for throughput.
- **text-generation-webui / oobabooga**
  - Pros: Flexible runtime supporting multiple backends (GPTQ, ExLlama, GGUF). Web UI + API layer.
  - Cons: Heavier footprint; may be overkill if custom chat UI is required.
- **vLLM**
  - Pros: High-throughput inference with paged attention, integrates with OpenAI-compatible API.
  - Cons: Prefers larger GPUs; RTX 3060 VRAM may limit max model size but smaller models (7B) should work.
- **LM Studio** (desktop tooling)
  - Pros: GUI management, local server mode.
  - Cons: Windows UI-driven, less automation; use as reference.
- **koboldcpp**
  - Pros: Balanced features, streaming API, good Windows support.
  - Cons: Smaller community than llama.cpp.

## Model Options
- **Instruction-tuned 7B/13B models** (e.g., `Nous Hermes 2`, `Mistral 7B Instruct`, `LLaMA 3 8B Instruct` in GGUF)
  - Fit within 12 GB VRAM at 4-5 bit quantization.
  - Provide good reasoning for transcript Q&A.
- **Smaller 3-4B models** for faster responses; fallback if latency is critical.
- Keep multiple quantizations stored on `z:/models/` to preserve SSD space.

## Embedding Models
- **sentence-transformers `all-MiniLM-L12-v2`** (CPU friendly, 384-dim)
  - Works via `sentence_transformers` lib; good baseline.
- **`intfloat/e5-large-v2`**
  - Higher accuracy; GPU acceleration beneficial.
- **local GGUF embedding models** via llama.cpp (e.g., `nomic-embed-text`) to stay fully offline.
- Ensure embeddings stored in float16/float32 to balance accuracy and size.

## Vector Stores
- **Qdrant**
  - Rust-based, can run via Docker with GPU support (optional). Suitable for network drive storage but prefer local SSD for performance.
- **Chroma**
  - Simple to embed in Python; stores data on disk (`duckdb + parquet`).
- **FAISS + SQLite/DuckDB**
  - Lightweight; good for initial prototype. Requires handling metadata persistence manually.
- **Weaviate (local)**
  - Heavier; might be overkill initially.

## Filesystem Watching & Ingestion
- **Python `watchdog`** or `watchfiles` for cross-platform directory monitoring.
- Debounce rapid events to avoid repeated reindex during large copy operations.
- Maintain queue (e.g., `asyncio` or `rq`) for ingestion tasks.
- Store file metadata (hash, modified time) to avoid redundant embedding.

## Transcript & Media Handling
- **Text transcripts**: chunk by semantic boundaries (paragraphs, timestamps).
- **Audio/Video**:
  - Use `faster-whisper` with GPU acceleration for transcription.
  - Cache transcripts on NAS with sidecar metadata (JSON) for reuse.
- Consider `yt-dlp` workflows for capturing video audio if needed.

## Chat UI Options
- **Frontend**: React + Vite + Tailwind; integrates with streaming API via WebSocket or Server-Sent Events.
- **State Management**: Zustand or Redux Toolkit for conversation history & settings.
- **Citation Display**: Highlight relevant passages, file paths, and timestamps.
- **User Controls**: Select knowledge base root, reindex button, model selection dropdown.

## Backend Stack
- **Python (FastAPI)**
  - Good balance between ecosystem and async support.
  - Integrations: `langchain` or `llama_index` OR custom minimal pipeline.
- **Node.js** (NestJS) as alternative; but Python has superior ML libraries.
- **Containerization**: Use Docker Compose to orchestrate backend, vector store, transcription service, optional UI build.

## Update Strategy
- Use incremental embeddings: if file changes, delete old vectors and insert new chunks.
- Maintain version history or snapshots for audit (store in SQLite).
- Provide progress notifications to UI via WebSocket events.

## Next Research Actions
- Benchmark candidate LLMs on RTX 3060 (7B instruct vs 13B) for latency and accuracy.
- Evaluate embedding accuracy and speed (MiniLM vs e5 vs nomic).
- Decide on vector store based on local storage constraints (likely FAISS + SQLite to start, with option to move to Qdrant).
- Investigate existing internal GitHub repo for LLM tooling once repository name/location is known.
