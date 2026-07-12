from fastapi import APIRouter, HTTPException, status

from app.api.schemas import AskRequest, AskResponse, HealthResponse
from app.service import ask_agent


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["system"],
)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post(
    "/ask",
    response_model=AskResponse,
    tags=["agent"],
)
def ask(request: AskRequest) -> AskResponse:
    try:
        answer = ask_agent(
            question=request.question,
            conversation_id=request.conversation_id,
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The agent is temporarily unavailable.",
        ) from error

    return AskResponse(
        answer=answer,
        conversation_id=request.conversation_id,
    )

