"""Collection of schemas for the API."""

from typing import Literal

from whyhow.schemas.base import BaseRequest, BaseResponse, BaseReturn
from whyhow.schemas.common import Graph, Schema

# Custom types
Status = Literal["success", "pending", "failure"]


class AddDocumentsResponse(BaseResponse):
    """Schema for the response body of the add documents endpoint."""

    namespace: str
    message: str


class CreateQuestionGraphRequest(BaseRequest):
    """Schema for the request body of the create graph endpoint."""

    questions: list[str]


class CreateSchemaGraphRequest(BaseRequest):
    """Schema for the request body of the create graph with schema endpoint."""

    graph_schema: Schema


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
    include_triples: bool = False
    include_chunks: bool = False


class QueryGraphTripleResponse(BaseResponse):
    """Schema for the triples within the query graph response."""

    head: str
    relation: str
    tail: str


class QueryGraphChunkResponse(BaseResponse):
    """Schema for the triples within the query graph response."""

    head: str
    relation: str
    tail: str
    chunk_ids: list[str]
    chunk_texts: list[str]


class QueryGraphResponse(BaseResponse):
    """Schema for the response body of the query graph endpoint."""

    namespace: str
    answer: str
    triples: list[QueryGraphTripleResponse] = []
    chunks: list[QueryGraphChunkResponse] = []


class QueryGraphReturn(BaseReturn):
    """Schema for the return value of the query graph endpoint."""

    namespace: str
    answer: str
    triples: list[QueryGraphTripleResponse] = []
    chunks: list[QueryGraphChunkResponse] = []


class SpecificQueryGraphRequest(BaseRequest):
    """Schema for the request body of the specific query graph endpoint."""

    query: str
    entities: list[str] = []
    relations: list[str] = []
    include_triples: bool = False
    include_chunks: bool = False


class SpecificQueryGraphResponse(BaseResponse):
    """Schema for the response body of the query graph endpoint."""

    namespace: str
    answer: str
    triples: list[dict[str, str]] = []
