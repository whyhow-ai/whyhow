"""Interacting with the graph API."""

import csv
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
    SpecificQueryGraphRequest,
    SpecificQueryGraphResponse,
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
            document_path.suffix in [".pdf", ".csv"]
            for document_path in document_paths
        ):
            raise ValueError("Only PDFs and CSVs are supported")

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

        if any(
            document_path.suffix == ".csv" for document_path in document_paths
        ):
            if len(document_paths) > 1:
                raise ValueError(
                    "Too many documents"
                    "Please limit CSV uploads to 1 file during the beta."
                )

        if len(document_paths) > 3:
            raise ValueError(
                "Too many documents"
                "Please limit PDF uploads to 3 files during the beta."
            )

        files = [
            (
                "documents",
                (document_path.name, open(document_path, "rb")),
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

    def generate_schema(self, documents: list[str]) -> str:
        """Generate a schema from CSV document."""
        if not documents:
            raise ValueError("No documents provided")

        document_paths = [Path(document) for document in documents]
        if not all(document_path.exists() for document_path in document_paths):
            raise ValueError("Not all documents exist")

        if not all(
            document_path.suffix in [".csv"]
            for document_path in document_paths
        ):
            raise ValueError(
                "Only CSVs are supported"
                "for local schema generation right now."
            )

        if any(
            document_path.suffix == ".csv" for document_path in document_paths
        ):
            if len(document_paths) > 1:
                raise ValueError(
                    "Too many documents"
                    "can only generate schema for one document at a time."
                )
        entities = []
        patterns = []

        with open(document_paths[0], newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                for i in range(len(row) - 1):
                    _pattern = {
                        "head": row[0],
                        "relation": (
                            f"has_{row[i+1].lower().replace(' ', '_')}"
                        ),
                        "tail": row[i + 1],
                        "description": "",
                    }
                    patterns.append(_pattern)
                for i in range(len(row)):
                    _entity = {
                        "name": row[i],
                        "set_type_as": "",
                        "property_columns": [],
                        "description": "",
                    }
                    entities.append(_entity)
                break

        return json.dumps(
            {"entities": entities, "patterns": patterns}, indent=4
        )

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

    def create_graph_from_csv(self, namespace: str, schema_file: str) -> str:
        """Create a new graph using a CSV based on a user-defined schema.

        Parameters
        ----------
        namespace : str
            The namespace of the graph to create.
        schema_file : str
            The schema file to use to build the graph.
        """
        if not schema_file:
            raise ValueError("No schema provided")

        with open(schema_file, "r", encoding="utf-8-sig") as file:
            schema_data = json.load(file)
            for entity in schema_data["entities"]:
                for property in entity["property_columns"]:
                    if property.lower() in ["name", "namespace"]:
                        raise ValueError(
                            f"The values 'name' and 'namespace'"
                            f"are not allowed in property_columns."
                            f"Found '{property}'."
                        )

        schema_model = SchemaModel(**schema_data)

        request_body = CreateSchemaGraphRequest(graph_schema=schema_model)

        raw_response = self.client.post(
            f"{self.prefix}/{namespace}/create_graph_from_csv",
            json=request_body.model_dump(),
        )

        raw_response.raise_for_status()

        response = CreateGraphResponse.model_validate(raw_response.json())

        return response.message

    def query_graph(
        self,
        namespace: str,
        query: str,
        include_triples: bool = False,
        include_chunks: bool = False,
    ) -> QueryGraphResponse:
        """Query the graph.

        Parameters
        ----------
        namespace : str
            The namespace of the graph.

        query : str
            The query to run.

        Returns
        -------
        QueryGraphResponse
            The namespace, answer, triples, and chunks and Cypher query.

        """
        request_body = QueryGraphRequest(
            query=query,
            include_triples=include_triples,
            include_chunks=include_chunks,
        )

        raw_response = self.client.post(
            f"{self.prefix}/{namespace}/query",
            json=request_body.model_dump(),
        )

        raw_response.raise_for_status()

        response = QueryGraphResponse.model_validate(raw_response.json())

        # retval = QueryGraphReturn(answer=response.answer)

        return response

    def query_graph_specific(
        self,
        namespace: str,
        query: str,
        entities: list[str] = [],
        relations: list[str] = [],
        include_triples: bool = False,
        include_chunks: bool = False,
    ) -> SpecificQueryGraphResponse:
        """Query the graph with specific entities and relations.

        Parameters
        ----------
        namespace : str
            The namespace of the graph.

        entities : list[str]
            The entities to query.

        relations : list[str]
            The relations to query.

        Returns
        -------
        SpecificQueryGraphResponse
            The namespace, answer, triples, and chunks.

        """
        request_body = SpecificQueryGraphRequest(
            query=query,
            entities=entities,
            relations=relations,
            include_triples=include_triples,
            include_chunks=include_chunks,
        )

        raw_response = self.client.post(
            f"{self.prefix}/{namespace}/specific_query",
            json=request_body.model_dump(),
        )

        raw_response.raise_for_status()

        response = SpecificQueryGraphResponse.model_validate(
            raw_response.json()
        )

        return response
