from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent


def create_application() -> FastAPI:
    application = FastAPI(
        title="HelpDesk AI Agent",
    )

    @application.get("/", include_in_schema=False)
    def landing_page():
        return FileResponse(
            BASE_DIR / "static" / "index.html"
        )

    application.include_router(router)

    return application
