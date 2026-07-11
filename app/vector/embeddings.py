from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings


embeddings = HuggingFaceEmbeddings(
    model_name=settings.embedding_model,
    model_kwargs={
        "device": "cpu",
    },
    encode_kwargs={
        "normalize_embeddings": True,
    },
)
