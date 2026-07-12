from fastapi import FastAPI

from app.api.routes import router


def create_application() -> FastAPI:
    application = FastAPI(
        title="HelpDesk AI Agent",
        description=(
            "An enterprise help-desk agent that combines structured "
            "database queries with semantic document retrieval."
        ),
        version="0.1.0",
    )

    application.include_router(router)

    return application


app = create_application()
