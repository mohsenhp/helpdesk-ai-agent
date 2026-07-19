import argparse

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    SearchField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)

from app.config import settings


def get_index_client() -> SearchIndexClient:
    if not settings.azure_search_endpoint:
        raise RuntimeError(
            "Azure Search endpoint is not configured"
        )

    if not settings.azure_search_api_key:
        raise RuntimeError(
            "Azure Search API key is not configured"
        )

    return SearchIndexClient(
        endpoint=settings.azure_search_endpoint,
        credential=AzureKeyCredential(
            settings.azure_search_api_key,
        ),
    )

def list_indexes(
    client: SearchIndexClient,
) -> None:
    indexes = list(client.list_indexes())

    if not indexes:
        print("No indexes found.")
        return

    print("Existing indexes:")

    for index in indexes:
        print(f"  - {index.name}")

def index_exists(
    client: SearchIndexClient,
) -> bool:
    try:
        client.get_index(
            settings.azure_search_index,
        )
        return True

    except ResourceNotFoundError:
        return False

def create_index(
    client: SearchIndexClient,
) -> None:

    definition = create_index_definition()

    client.create_index(
        definition
    )

    print(
        f"Created index: {definition.name}"
    )

def create_index_definition() -> SearchIndex:
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True,
        ),

        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
        ),

        SearchableField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True,
        ),

        SearchableField(
            name="file_name",
            type=SearchFieldDataType.String,
            filterable=True,
        ),

        SimpleField(
            name="document_type",
            type=SearchFieldDataType.String,
            filterable=True,
            searchable=False,
        ),

        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(
                SearchFieldDataType.Single
            ),
            searchable=True,
            vector_search_dimensions=384,
            vector_search_profile_name="vector-profile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="hnsw-config",
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config",
            )
        ],
    )

    return SearchIndex(
        name=settings.azure_search_index,
        fields=fields,
        vector_search=vector_search,
    )

def delete_index(
    client: SearchIndexClient,
) -> None:
    client.delete_index(
        settings.azure_search_index,
    )

    print(
        f"Deleted index: {settings.azure_search_index}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete and recreate the Azure Search index",
    )

    args = parser.parse_args()

    client = get_index_client()

    print(
        f"Connected to Azure AI Search: "
        f"{settings.azure_search_endpoint}"
    )

    print()

    if index_exists(client):

        if args.recreate:
            print(
                f"Recreating index: "
                f"{settings.azure_search_index}"
            )

            delete_index(client)

        else:
            print(
                f"Index '{settings.azure_search_index}' already exists."
            )

            return

    create_index(client)


if __name__ == "__main__":
    main()
