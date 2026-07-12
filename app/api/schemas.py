from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    status: str


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="The help-desk question to send to the agent.",
    )

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError("Question must not be blank.")

        return stripped_value


class AskResponse(BaseModel):
    answer: str
