"""Tests focused on the graph API."""

import os

import pytest

from whyhow.client import WhyHow
from whyhow.schemas.common import Graph, Node, Relationship
from whyhow.schemas.graph import (
    QueryGraphRequest,
    QueryGraphResponse,
    QueryGraphReturn,
)

# Set fake environment variables
os.environ["WHYHOW_API_KEY"] = "fake_api_key"
os.environ["OPENAI_API_KEY"] = "fake_openai_key"
os.environ["PINECONE_API_KEY"] = "fake_pinecone_key"
os.environ["NEO4J_USER"] = "fake_neo4j_user"
os.environ["NEO4J_PASSWORD"] = "fake_neo4j_password"
os.environ["NEO4J_URL"] = "fake_neo4j_url"

EXAMPLE_GRAPH = Graph(
    relationships=[
        Relationship(
            type="knows",
            start_node=Node(labels=["Person"], properties={"name": "Alice"}),
            end_node=Node(labels=["Person"], properties={"name": "Bob"}),
            properties={"since": "2022-01-01"},
        )
    ]
)


class TestGraphAPIQuery:
    def test_query_graph(self, httpx_mock):
        client = WhyHow()
        query = "What friends does Alice have?"

        fake_response_body = QueryGraphResponse(
            namespace="something",
            answer="Alice knows Bob",
        )
        httpx_mock.add_response(
            method="POST",
            json=fake_response_body.model_dump(),
        )

        result = client.graph.query_graph(
            namespace="something",
            query=query,
        )

        assert result == QueryGraphReturn(answer="Alice knows Bob")

        actual_request = httpx_mock.get_requests()[0]
        expected_request_body = QueryGraphRequest(query=query)
        actual_request_body = QueryGraphRequest.model_validate_json(
            actual_request.read().decode()
        )

        assert actual_request.url.path == "/graphs/something/query"
        assert actual_request_body == expected_request_body


class TestGraphAPIAddDocuments:

    def test_errors(self, httpx_mock, tmp_path):
        client = WhyHow()

        with pytest.raises(ValueError, match="No documents provided"):
            client.graph.add_documents("something", documents=[])

        tmp_pdf_1 = tmp_path / "example.pdf"
        tmp_pdf_1.touch()
        tmp_pdf_2 = tmp_path / "example2.wav"

        with pytest.raises(ValueError, match="Not all documents exist"):
            client.graph.add_documents(
                "something",
                documents=[tmp_pdf_1, tmp_pdf_2],
            )

        tmp_pdf_2.touch()

        with pytest.raises(ValueError, match="Only PDFs are supported"):
            client.graph.add_documents(
                "something",
                documents=[tmp_pdf_1, tmp_pdf_2],
            )
