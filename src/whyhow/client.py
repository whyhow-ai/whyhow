"""Implementation of the client logic."""

import os
from typing import Any, Generator, Optional

from httpx import AsyncClient, Auth, Client, Request, Response

from whyhow.apis.graph import GraphAPI

BASE_URL = "https://43nq5c1b4c.execute-api.us-east-2.amazonaws.com"


class APIKeyAuth(Auth):
    """Authorization header with API key."""

    def __init__(
        self,
        api_key: str,
        pinecone_api_key: str,
        neo4j_url: str,
        neo4j_user: str,
        neo4j_password: str,
        model_type: str,
        openai_api_key: Optional[str] = None,
        azure_openai_api_key: Optional[str] = None,
        azure_openai_version: Optional[str] = None,
        azure_openai_endpoint: Optional[str] = None,
        use_azure: bool = False,
    ) -> None:
        """Initialize the auth object."""
        if openai_api_key is not None and azure_openai_api_key is not None:
            raise ValueError(
                "Only one of openai_api_key or"
                "azure_openai_api_key should be set."
            )

        self.api_key = api_key
        self.pinecone_api_key = pinecone_api_key
        self.neo4j_url = neo4j_url
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.model_type = model_type
        self.openai_api_key = openai_api_key
        self.azure_openai_api_key = azure_openai_api_key
        self.azure_openai_version = azure_openai_version
        self.azure_openai_endpoint = azure_openai_endpoint
        self.use_azure = use_azure

    def auth_flow(
        self, request: Request
    ) -> Generator[Request, Response, None]:
        """Add the API key to the request."""
        request.headers["x-api-key"] = self.api_key
        request.headers["x-pinecone-key"] = self.pinecone_api_key
        if self.openai_api_key is not None:
            request.headers["x-openai-key"] = self.openai_api_key
        elif self.azure_openai_api_key is not None:
            request.headers["x-azure-openai-key"] = self.azure_openai_api_key
            if self.azure_openai_version is not None:
                request.headers["x-azure-openai-version"] = (
                    self.azure_openai_version
                )
            if self.azure_openai_endpoint is not None:
                request.headers["x-azure-openai-endpoint"] = (
                    self.azure_openai_endpoint
                )
        request.headers["x-neo4j-user"] = self.neo4j_user
        request.headers["x-neo4j-password"] = self.neo4j_password
        request.headers["x-neo4j-url"] = self.neo4j_url
        request.headers["x-model-type"] = self.model_type

        if self.use_azure:
            request.headers["x-use-azure"] = "true"

        yield request


class WhyHow:
    """Synchronous client for the WhyHow API.

    Parameters
    ----------
    api_key : str, optional
        The API key to use for authentication. If not provided, the
        WHYHOW_API_KEY environment variable will be used.

    base_url : str, optional
        The base URL for the API.

    httpx_kwargs : dict, optional
        Additional keyword arguments to pass to the httpx client.

    Attributes
    ----------
    httpx_client : httpx.Client
        A synchronous httpx client.
    """

    def __init__(
        self,
        api_key: str | None = None,
        pinecone_api_key: str | None = None,
        neo4j_url: str | None = None,
        neo4j_user: str | None = None,
        neo4j_password: str | None = None,
        model_type: Optional[str] | None = None,
        openai_api_key: str | None = None,
        azure_openai_api_key: str | None = None,
        azure_openai_version: str | None = None,
        azure_openai_endpoint: str | None = None,
        base_url: str = BASE_URL,
        use_azure: bool = False,
        httpx_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the client."""
        if httpx_kwargs is None:
            httpx_kwargs = {}

        if api_key is None:
            api_key = os.environ.get("WHYHOW_API_KEY")

            if api_key is None:
                raise ValueError("WHYHOW_API_KEY must be set.")

        if pinecone_api_key is None:
            pinecone_api_key = os.environ.get("PINECONE_API_KEY")

            if pinecone_api_key is None:
                raise ValueError("PINECONE_API_KEY must be set.")

        if model_type is None:
            model_type = os.environ.get("MODEL_TYPE")

            if model_type is None:
                model_type = "general"

            elif model_type not in ["general", "health"]:
                print("Invalid model type. Using general model.")
                model_type = "general"

        if openai_api_key is None:
            openai_api_key = os.environ.get("OPENAI_API_KEY")

        if azure_openai_api_key is None:
            azure_openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")

        if openai_api_key is None and azure_openai_api_key is None:
            raise ValueError(
                "At least one of OPENAI_API_KEY"
                "or AZURE_OPENAI_API_KEY must be set."
            )

        if azure_openai_version is None:
            azure_openai_version = os.environ.get("AZURE_OPENAI_VERSION")

            if (
                azure_openai_api_key is not None
                and azure_openai_version is None
            ):
                raise ValueError("AZURE_OPENAI_VERSION must be set.")

        if azure_openai_endpoint is None:
            azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")

            if (
                azure_openai_api_key is not None
                and azure_openai_endpoint is None
            ):
                raise ValueError("AZURE_OPENAI_ENDPOINT must be set.")

        if neo4j_user is None:
            neo4j_user = os.environ.get("NEO4J_USER")

            if neo4j_user is None:
                raise ValueError("NEO4J_USER must be set.")

        if neo4j_password is None:
            neo4j_password = os.environ.get("NEO4J_PASSWORD")

            if neo4j_password is None:
                raise ValueError("NEO4J_PASSWORD must be set.")

        if neo4j_url is None:
            neo4j_url = os.environ.get("NEO4J_URL")

            if neo4j_url is None:
                raise ValueError("NEO4J_URL must be set.")

        auth = APIKeyAuth(
            api_key,
            pinecone_api_key,
            neo4j_url,
            neo4j_user,
            neo4j_password,
            model_type,
            openai_api_key,
            azure_openai_api_key,
            azure_openai_version,
            azure_openai_endpoint,
            use_azure,
        )

        if "base_url" in httpx_kwargs:
            raise ValueError("base_url cannot be set in httpx_kwargs.")

        httpx_kwargs["timeout"] = 60.0  # Set timeout to 30 seconds

        self.httpx_client = Client(
            base_url=base_url,
            auth=auth,
            **httpx_kwargs,
        )

        self.graph = GraphAPI(client=self.httpx_client, prefix="/graphs")


class AsyncWhyHow:
    """Asynchronous client for the WhyHow API.

    Parameters
    ----------
    api_key : str, optional
        The API key to use for authentication. If not provided, the
        WHYHOW_API_KEY environment variable will be used.

    base_url : str, optional
        The base URL for the API.

    httpx_kwargs : dict, optional
        Additional keyword arguments to pass to the httpx async client.

    Attributes
    ----------
    httpx_client : httpx.AsyncClient
        An async httpx client.
    """

    def __init__(
        self,
        api_key: str | None = None,
        pinecone_api_key: str | None = None,
        openai_api_key: str | None = None,
        neo4j_user: str | None = None,
        neo4j_password: str | None = None,
        neo4j_url: str | None = None,
        model_type: Optional[str] | None = None,
        base_url: str = BASE_URL,
        httpx_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the client."""
        if httpx_kwargs is None:
            httpx_kwargs = {}

        if api_key is None:
            api_key = os.environ.get("WHYHOW_API_KEY")

            if api_key is None:
                raise ValueError("WHYHOW_API_KEY must be set.")

        if pinecone_api_key is None:
            pinecone_api_key = os.environ.get("PINECONE_API_KEY")

            if pinecone_api_key is None:
                raise ValueError("PINECONE_API_KEY must be set.")

        if model_type is None:
            model_type = os.environ.get("MODEL_TYPE")

            if model_type is None:
                model_type = "general"

            elif model_type not in ["general", "health"]:
                print("Invalid model type. Using general model.")
                model_type = "general"

        if openai_api_key is None:
            openai_api_key = os.environ.get("OPENAI_API_KEY")

            if openai_api_key is None:
                raise ValueError("OPENAI_API_KEY must be set.")

        if neo4j_user is None:
            neo4j_user = os.environ.get("NEO4J_USER")

            if neo4j_user is None:
                raise ValueError("NEO4J_USER must be set.")

        if neo4j_password is None:
            neo4j_password = os.environ.get("NEO4J_PASSWORD")

            if neo4j_password is None:
                raise ValueError("NEO4J_PASSWORD must be set.")

        if neo4j_url is None:
            neo4j_url = os.environ.get("NEO4J_URL")

            if neo4j_url is None:
                raise ValueError("NEO4J_URL must be set.")

        auth = APIKeyAuth(
            api_key,
            pinecone_api_key,
            openai_api_key,
            neo4j_user,
            neo4j_password,
            neo4j_url,
            model_type,
        )

        if "base_url" in httpx_kwargs:
            raise ValueError("base_url cannot be set in httpx_kwargs.")

        self.httpx_client = AsyncClient(
            base_url=base_url,
            auth=auth,
            **httpx_kwargs,
        )
