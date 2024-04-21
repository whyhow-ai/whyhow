Here's the generated `api.md` file for your mkdocs based on the provided code files:

```markdown
# API Reference

This document provides a reference for the WhyHow API, which allows you to interact with the graph functionality.

## GraphAPI

The `GraphAPI` class provides methods to interact with the graph API synchronously.

### `add_documents`

```python
def add_documents(self, namespace: str, documents: list[str]) -> str
```

Add documents to the graph.

#### Parameters

- `namespace` (str): The namespace of the graph.
- `documents` (list[str]): The documents to add.

#### Returns

- (str): The response message.

#### Raises

- `ValueError`: If no documents are provided, not all documents exist, only PDFs are supported, PDFs are too large (limit: 8MB), or too many documents are provided (limit: 3 files during the beta).

### `create_graph`

```python
def create_graph(self, namespace: str, questions: list[str]) -> str
```

Create a new graph.

#### Parameters

- `namespace` (str): The namespace of the graph to create.
- `questions` (list[str]): The seed concepts to initialize the graph with.

#### Returns

- (str): The response message.

#### Raises

- `ValueError`: If no questions are provided.

### `create_graph_from_schema`

```python
def create_graph_from_schema(self, namespace: str, schema_file: str) -> str
```

Create a new graph based on a user-defined schema.

#### Parameters

- `namespace` (str): The namespace of the graph to create.
- `schema_file` (str): The schema file to use to build the graph.

#### Returns

- (str): The response message.

#### Raises

- `ValueError`: If no schema is provided.

### `query_graph`

```python
def query_graph(self, namespace: str, query: str) -> QueryGraphReturn
```

Query the graph.

#### Parameters

- `namespace` (str): The namespace of the graph.
- `query` (str): The query to run.

#### Returns

- (`QueryGraphReturn`): The answer, triples, and Cypher query.

## Schemas

The WhyHow API uses Pydantic models to define the request and response schemas.

### `AddDocumentsResponse`

```python
class AddDocumentsResponse(BaseResponse):
    """Schema for the response body of the add documents endpoint."""

    namespace: str
    message: str
```

### `CreateQuestionGraphRequest`

```python
class CreateQuestionGraphRequest(BaseRequest):
    """Schema for the request body of the create graph endpoint."""

    questions: list[str]
```

### `CreateSchemaGraphRequest`

```python
class CreateSchemaGraphRequest(BaseRequest):
    """Schema for the request body of the create graph endpoint."""

    graph_schema: SchemaModel
```

### `CreateGraphResponse`

```python
class CreateGraphResponse(BaseResponse):
    """Schema for the response body of the create graph endpoint."""

    namespace: str
    message: str
```

### `QueryGraphRequest`

```python
class QueryGraphRequest(BaseRequest):
    """Schema for the request body of the query graph endpoint."""

    query: str
```

### `QueryGraphResponse`

```python
class QueryGraphResponse(BaseResponse):
    """Schema for the response body of the query graph endpoint."""

    namespace: str
    answer: str
```

### `QueryGraphReturn`

```python
class QueryGraphReturn(BaseReturn):
    """Schema for the return value of the query graph endpoint."""

    answer: str
```

## Base Classes

The WhyHow API uses the following base classes for the API schemas:

### `APIBase`

```python
class APIBase(BaseModel, ABC):
    """Base class for API schemas."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: Client
    prefix: str = ""
```

### `AsyncAPIBase`

```python
class AsyncAPIBase(BaseModel, ABC):
    """Base class for async API schemas."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: AsyncClient
    prefix: str = ""
```
```

This `api.md` file provides an overview of the `GraphAPI` class and its methods, along with the request and response schemas used by the API. It also includes information about the base classes used for the API schemas.

You can include this file in your mkdocs documentation to provide a reference for the WhyHow API.