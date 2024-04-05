"""Collection of schemas for the API."""

from typing import Literal

from whyhow.schemas.base import BaseRequest, BaseResponse, BaseReturn
from whyhow.schemas.common import Graph

# Custom types
Status = Literal["success", "pending", "failure"]


class AddDocumentsResponse(BaseResponse):
    """Schema for the response body of the add documents endpoint."""

    namespace: str
    message: str


# Request and response schemas
class CreateGraphResponse(BaseResponse):
    """Schema for the response body of the create graph endpoint."""

    namespace: str
    message: str


class GetGraphResponse(BaseResponse):
    """Schema for the response body of the get graph endpoint."""

    namespace: str
    status: Status
    documents: list[str]
    graph: Graph


class QueryGraphRequest(BaseRequest):
    """Schema for the request body of the query graph endpoint."""

    query: str


class QueryGraphResponse(BaseResponse):
    """Schema for the response body of the query graph endpoint."""

    namespace: str
    answer: str


class QueryGraphReturn(BaseReturn):
    """Schema for the return value of the query graph endpoint."""

    answer: str
