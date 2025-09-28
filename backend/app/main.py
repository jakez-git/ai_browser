from fastapi import FastAPI

from .routers import chat, health


def create_app() -> FastAPI:
    """Instantiate and configure the FastAPI application."""
    app = FastAPI(title="Local Chat Knowledge Base")

    app.include_router(health.router)
    app.include_router(chat.router)

    return app


app = create_app()
