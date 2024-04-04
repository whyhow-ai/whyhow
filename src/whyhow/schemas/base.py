"""Base classes for request, response, and return schemas."""

from abc import ABC

from pydantic import BaseModel, ConfigDict


class BaseRequest(BaseModel, ABC):
    """Base class for all request schemas."""

    model_config = ConfigDict(extra="forbid")


class BaseResponse(BaseModel, ABC):
    """Base class for all response schemas.

    Since the API can change, we want to ignore any extra fields that are not
    defined in the schema.
    """

    model_config = ConfigDict(extra="ignore")


class BaseReturn(BaseModel, ABC):
    """Base class for return schemas."""

    model_config = ConfigDict(extra="forbid")
