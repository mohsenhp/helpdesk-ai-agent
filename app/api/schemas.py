from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    status: str


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="The help-desk question to send to the agent.",
    )
    conversation_id: str = Field(
        default_factory=lambda: str(uuid4()),
        min_length=1,
        max_length=128,
        description=(
            "Identifier used to continue an existing conversation."
        ),
    )

    @field_validator("question", "conversation_id")
    @classmethod
    def value_must_not_be_blank(
        cls,
        value: str,
    ) -> str:
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError(
                "Value must not be blank."
            )

        return stripped_value


class AskResponse(BaseModel):
    answer: str
    conversation_id: str
