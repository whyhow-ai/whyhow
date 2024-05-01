"""Tests focused on the graph API."""

import os
from unittest.mock import Mock

import pytest

from whyhow.client import WhyHow
from whyhow.schemas.common import Graph, Node, Relationship
from whyhow.schemas.graph import (
    QueryGraphRequest,
    QueryGraphResponse,
    QueryGraphReturn,
)
from whyhow.validations import VerifyConnectivity

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
    """Tests for the query_graph method."""

    def test_query_graph(self, httpx_mock, monkeypatch):
        """Test querying the graph."""
        connectivity_client = Mock(spec=VerifyConnectivity)
        connectivity_client.return_value = None
        monkeypatch.setattr(
            "whyhow.client.VerifyConnectivity", connectivity_client
        )

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
    """Tests for the add_documents method."""

    def test_errors(self, monkeypatch, tmp_path):
        """Test error handling."""
        connectivity_client = Mock(spec=VerifyConnectivity)
        connectivity_client.return_value = None
        monkeypatch.setattr(
            "whyhow.client.VerifyConnectivity", connectivity_client
        )

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
