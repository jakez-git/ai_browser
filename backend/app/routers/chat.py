from fastapi import APIRouter, Depends, HTTPException, status

from ..models import ChatRequest, ChatResponse
from ..services.chat_service import ChatService, get_chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/query", response_model=ChatResponse)
async def query_chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Handle chat requests using retrieval-augmented generation."""
    try:
        return await chat_service.generate_response(request)
    except ValueError as exc:  # pragma: no cover - refined in service tests
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
