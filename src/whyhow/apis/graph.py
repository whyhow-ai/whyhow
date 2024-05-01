"""Interacting with the graph API."""

import json
import os
from pathlib import Path

from whyhow.apis.base import APIBase
from whyhow.schemas.common import Schema as SchemaModel
from whyhow.schemas.graph import (
    AddDocumentsResponse,
    CreateGraphResponse,
    CreateQuestionGraphRequest,
    CreateSchemaGraphRequest,
    QueryGraphRequest,
    QueryGraphResponse,
    QueryGraphReturn,
)


class GraphAPI(APIBase):
    """Interacting with the graph API synchronously."""

    def add_documents(self, namespace: str, documents: list[str]) -> str:
        """Add documents to the graph.

        Parameters
        ----------
        namespace : str
            The namespace of the graph.

        documents : list[str]
            The documents to add.
        """
        if not documents:
            raise ValueError("No documents provided")

        document_paths = [Path(document) for document in documents]
        if not all(document_path.exists() for document_path in document_paths):
            raise ValueError("Not all documents exist")

        if not all(
            document_path.suffix == ".pdf" for document_path in document_paths
        ):
            raise ValueError("Only PDFs are supported")

        if (
            sum(
                os.path.getsize(document_path)
                for document_path in document_paths
            )
            > 8388600
        ):
            raise ValueError(
                "PDFs too large, please limit your total upload size to <8MB."
            )

        if len(document_paths) > 3:
            raise ValueError("""Too many documents
                please limit uploads to 3 files during the beta.""")

        files = [
            (
                "documents",
                (
                    document_path.name,
                    open(document_path, "rb"),
                    "application/pdf",
                ),
            )
            for document_path in document_paths
        ]

        raw_response = self.client.post(
            f"{self.prefix}/{namespace}/add_documents",
            files=files,
        )

        raw_response.raise_for_status()

        response = AddDocumentsResponse.model_validate(raw_response.json())

        return response.message

    def create_graph(self, namespace: str, questions: list[str]) -> str:
        """Create a new graph.

        Parameters
        ----------
        namespace : str
            The namespace of the graph to create.
        questions : list[str]
            The seed concepts to initialize the graph with.
        """
        if not questions:
            raise ValueError("No questions provided")

        request_body = CreateQuestionGraphRequest(questions=questions)

        raw_response = self.client.post(
            f"{self.prefix}/{namespace}/create_graph",
            json=request_body.model_dump(),
        )

        raw_response.raise_for_status()

        response = CreateGraphResponse.model_validate(raw_response.json())

        return response.message

    def create_graph_from_schema(
        self, namespace: str, schema_file: str
    ) -> str:
        """Create a new graph based on a user-defined schema.

        Parameters
        ----------
        namespace : str
            The namespace of the graph to create.
        schema_file : str
            The schema file to use to build the graph.
        """
        if not schema_file:
            raise ValueError("No schema provided")

        with open(schema_file, "r") as file:
            schema_data = json.load(file)

        schema_model = SchemaModel(**schema_data)

        request_body = CreateSchemaGraphRequest(graph_schema=schema_model)

        raw_response = self.client.post(
            f"{self.prefix}/{namespace}/create_graph_from_schema",
            json=request_body.model_dump(),
        )

        raw_response.raise_for_status()

        response = CreateGraphResponse.model_validate(raw_response.json())

        return response.message

    def query_graph(self, namespace: str, query: str) -> QueryGraphReturn:
        """Query the graph.

        Parameters
        ----------
        namespace : str
            The namespace of the graph.

        query : str
            The query to run.

        Returns
        -------
        QueryGraphReturn
            The answer, triples, and Cypher query.

        """
        request_body = QueryGraphRequest(query=query)

        raw_response = self.client.post(
            f"{self.prefix}/{namespace}/query",
            json=request_body.model_dump(),
        )

        raw_response.raise_for_status()

        response = QueryGraphResponse.model_validate(raw_response.json())

        retval = QueryGraphReturn(answer=response.answer)

        return retval
