from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    google_api_key: str
    gemini_model: str


settings = Settings(
    google_api_key=os.environ["GOOGLE_API_KEY"],
    gemini_model=os.getenv(
        "GEMINI_MODEL",
        "gemini-3.1-flash-lite",
    ),
)