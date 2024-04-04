"""Base classes for API schemas."""

from abc import ABC

from httpx import AsyncClient, Client
from pydantic import BaseModel, ConfigDict


class APIBase(BaseModel, ABC):
    """Base class for API schemas."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: Client
    prefix: str = ""


class AsyncAPIBase(BaseModel, ABC):
    """Base class for async API schemas."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: AsyncClient
    prefix: str = ""
