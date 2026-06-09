"""Etymolt SDK client. Sync + async."""

from __future__ import annotations

import os
from datetime import datetime, timezone, timedelta
from typing import Any, Optional, Union

import httpx

from .types import Verdict


class EtymoltError(Exception):
    """Raised when the Etymolt API returns a non-2xx response."""

    def __init__(self, message: str, status: Optional[int] = None, response: Any = None):
        super().__init__(message)
        self.status = status
        self.response = response


class Etymolt:
    """
    Synchronous Etymolt client.

    >>> from etymolt import Etymolt
    >>> etymolt = Etymolt()
    >>> verdict = etymolt.verify("Stratagem")
    >>> verdict["verdict"]
    'ITERATE'

    Free tier requires no API key. Pass ``api_key`` or set the
    ``ETYMOLT_API_KEY`` environment variable to authenticate.
    """

    DEFAULT_BASE_URL = "https://api.etymolt.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        client: Optional[httpx.Client] = None,
        timeout: float = 30.0,
    ):
        self._base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self._api_key = api_key or os.environ.get("ETYMOLT_API_KEY")
        self._client = client or httpx.Client(timeout=timeout)
        self._own_client = client is None

    def __enter__(self) -> "Etymolt":
        return self

    def __exit__(self, *exc: Any) -> None:
        if self._own_client:
            self._client.close()

    def verify(
        self,
        name: str,
        *,
        nice_classes: Optional[list[int]] = None,
    ) -> Verdict:
        """
        Verify a candidate name. Returns a signed EVP/1 verdict.

        :param name: The candidate name to verify.
        :param nice_classes: Optional NICE classification numbers for the
            goods/services your name will be filed against.
        """
        body: dict[str, Any] = {"name": name}
        if nice_classes:
            body["nice_classes"] = nice_classes

        headers = {"content-type": "application/json"}
        if self._api_key:
            headers["x-etymolt-key"] = self._api_key

        response = self._client.post(
            f"{self._base_url}/v1/verify",
            json=body,
            headers=headers,
        )

        if response.status_code >= 400:
            payload: Any = None
            try:
                payload = response.json()
            except Exception:
                pass
            raise EtymoltError(
                f"Etymolt API returned {response.status_code}: {response.reason_phrase}",
                status=response.status_code,
                response=payload,
            )

        return response.json()  # type: ignore[no-any-return]

    @staticmethod
    def is_stale(verdict: Verdict, now: Optional[datetime] = None) -> bool:
        """Check whether a verdict is past its valid_until boundary."""
        current = now or datetime.now(timezone.utc)
        if "valid_until" in verdict and verdict["valid_until"]:
            valid_until = datetime.fromisoformat(verdict["valid_until"].replace("Z", "+00:00"))
            return current > valid_until
        # Default policy: stale after 24h if no explicit valid_until.
        issued = datetime.fromisoformat(verdict["issued_at"].replace("Z", "+00:00"))
        return current - issued > timedelta(hours=24)

    @staticmethod
    def age(verdict: Verdict, now: Optional[datetime] = None) -> timedelta:
        """Get the age of a verdict."""
        current = now or datetime.now(timezone.utc)
        issued = datetime.fromisoformat(verdict["issued_at"].replace("Z", "+00:00"))
        return current - issued


class AsyncEtymolt:
    """
    Asynchronous Etymolt client.

    >>> from etymolt import AsyncEtymolt
    >>> async with AsyncEtymolt() as etymolt:
    ...     verdict = await etymolt.verify("Stratagem")
    """

    DEFAULT_BASE_URL = "https://api.etymolt.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 30.0,
    ):
        self._base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self._api_key = api_key or os.environ.get("ETYMOLT_API_KEY")
        self._client = client or httpx.AsyncClient(timeout=timeout)
        self._own_client = client is None

    async def __aenter__(self) -> "AsyncEtymolt":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._own_client:
            await self._client.aclose()

    async def verify(
        self,
        name: str,
        *,
        nice_classes: Optional[list[int]] = None,
    ) -> Verdict:
        """Verify a candidate name asynchronously."""
        body: dict[str, Any] = {"name": name}
        if nice_classes:
            body["nice_classes"] = nice_classes

        headers = {"content-type": "application/json"}
        if self._api_key:
            headers["x-etymolt-key"] = self._api_key

        response = await self._client.post(
            f"{self._base_url}/v1/verify",
            json=body,
            headers=headers,
        )

        if response.status_code >= 400:
            payload: Any = None
            try:
                payload = response.json()
            except Exception:
                pass
            raise EtymoltError(
                f"Etymolt API returned {response.status_code}: {response.reason_phrase}",
                status=response.status_code,
                response=payload,
            )

        return response.json()  # type: ignore[no-any-return]
