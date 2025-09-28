from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ping")
def ping() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "ok"}
