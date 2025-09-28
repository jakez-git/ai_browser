from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(..., description="User prompt for the LLM")
    top_k: int | None = Field(5, ge=1, le=20, description="Maximum retrieved chunks")
    stream: bool = Field(False, description="Enable streaming responses")


class ChatResponse(BaseModel):
    response: str = Field(..., description="LLM generated reply")
    sources: list[str] = Field(default_factory=list, description="List of cited knowledge sources")
