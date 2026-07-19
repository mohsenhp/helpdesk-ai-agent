from fastapi import APIRouter, HTTPException

from app.api.schemas import AskRequest, AskResponse, HealthResponse, MetadataResponse
from app.service import ask_agent
from app.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["system"],
)
def health_check() -> HealthResponse:
    settings = get_settings()

    return HealthResponse(
        status="ok",
        environment=settings.environment,
    )


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
    except Exception:
        logger.exception(
            "Unhandled exception while processing /ask"
        )

        raise HTTPException(
            status_code=503,
            detail="The agent is temporarily unavailable.",
        )

    return AskResponse(
        answer=answer,
        conversation_id=request.conversation_id,
    )


@router.get(
    "/metadata",
    response_model=MetadataResponse,
    tags=["system"],
)
def metadata() -> MetadataResponse:
    settings = get_settings()

    return MetadataResponse(
        name="HelpDesk AI Agent",
        version="0.1.0",
        capabilities=[
            "ticket_search",
            "incident_analysis",
            "knowledge_base_search",
        ],
        environment=settings.environment,
    )

