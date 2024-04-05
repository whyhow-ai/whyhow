"""Tests for the client module."""

from unittest.mock import Mock

import pytest
from httpx import Client

from whyhow.client import WhyHow


class TestWhyHow:
    def test_constructor_missing_api_key(self, monkeypatch):
        monkeypatch.delenv("WHYHOW_API_KEY", raising=False)
        with pytest.raises(ValueError, match="WHYHOW_API_KEY must be set"):
            WhyHow()

    def test_httpx_kwargs(self, monkeypatch):
        fake_httpx_client_inst = Mock(spec=Client)
        fake_httpx_client_class = Mock(return_value=fake_httpx_client_inst)

        monkeypatch.setattr("whyhow.client.Client", fake_httpx_client_class)
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

    def test_base_url_twice(self):
        with pytest.raises(
            ValueError, match="base_url cannot be set in httpx_kwargs."
        ):
            WhyHow(
                api_key="key",
                httpx_kwargs={"base_url": "https://example.com"},
            )
