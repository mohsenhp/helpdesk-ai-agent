from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agent.checkpoint import close_checkpoint_resources
from app.api.routes import router


@asynccontextmanager
async def lifespan(
    application: FastAPI,
) -> AsyncIterator[None]:
    yield
    close_checkpoint_resources()


def create_application() -> FastAPI:
    application = FastAPI(
        title="HelpDesk AI Agent",
        description=(
            "An enterprise help-desk agent that combines structured "
            "database queries with semantic document retrieval."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )

    application.include_router(router)

    return application


app = create_application()
