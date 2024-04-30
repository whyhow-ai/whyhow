"""Tests for the client module."""

from unittest.mock import Mock

import pytest
from httpx import Client
from neo4j.exceptions import ConfigurationError

from whyhow.client import WhyHow
from whyhow.validations import VerifyConnectivity


class TestWhyHow:
    """Tests for the WhyHow class."""

    def test_constructor_missing_api_key(self, monkeypatch):
        """Test creating a WhyHow instance without an API key."""
        monkeypatch.delenv("WHYHOW_API_KEY", raising=False)
        with pytest.raises(ValueError, match="WHYHOW_API_KEY must be set"):
            WhyHow()

    def test_httpx_kwargs(self, monkeypatch):
        """Test passing httpx_kwargs to the constructor."""
        fake_httpx_client_inst = Mock(spec=Client)
        fake_httpx_client_class = Mock(return_value=fake_httpx_client_inst)

        monkeypatch.setattr("whyhow.client.Client", fake_httpx_client_class)

        connectivity_client = Mock(spec=VerifyConnectivity)
        connectivity_client.return_value = None
        monkeypatch.setattr(
            "whyhow.client.VerifyConnectivity", connectivity_client
        )

        httpx_kwargs = {"verify": False}
        client = WhyHow(
            api_key="key",
            httpx_kwargs=httpx_kwargs,
        )

        assert fake_httpx_client_class.call_count == 1
        args, kwargs = fake_httpx_client_class.call_args

        assert not args
        assert (
            kwargs["base_url"]
            == "https://43nq5c1b4c.execute-api.us-east-2.amazonaws.com"
        )
        assert not kwargs["verify"]

        assert client.httpx_client is fake_httpx_client_class.return_value

    def test_credentials_verification(self, monkeypatch):
        connectivity_client = Mock(spec=VerifyConnectivity)
        connectivity_client.side_effect = ConfigurationError(
            "Invalid credentials"
        )
        monkeypatch.setattr(
            "whyhow.client.VerifyConnectivity", connectivity_client
        )
        with pytest.raises(ConfigurationError) as exc_info:
            WhyHow(
                api_key="mock_api_key",
                neo4j_user="mock_neo4j_user",
                neo4j_url="mock_neo4j_url",
                neo4j_password="mock_neo4j_password",
                pinecone_api_key="mock_pinecone_api_key",
            )
        assert "Invalid credentials" in str(
            exc_info.value
        ), "The exception message is not as expected"

    def test_base_url_twice(self, monkeypatch):
        """Test setting base_url in httpx_kwargs."""
        connectivity_client = Mock(spec=VerifyConnectivity)
        connectivity_client.return_value = None
        monkeypatch.setattr(
            "whyhow.client.VerifyConnectivity", connectivity_client
        )

        with pytest.raises(
            ValueError, match="base_url cannot be set in httpx_kwargs."
        ):
            WhyHow(
                api_key="key",
                httpx_kwargs={"base_url": "https://example.com"},
            )
