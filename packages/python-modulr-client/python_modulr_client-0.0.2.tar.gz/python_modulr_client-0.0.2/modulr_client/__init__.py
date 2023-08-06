from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Optional
from wsgiref.handlers import format_date_time

from modulr_client.client import Client
from modulr_client.signature import calculate


class ModulrClient(Client):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        hmac: str,
        nonce: Optional[str] = None,
        retry: bool = False,
    ):
        self._api_key = api_key
        self._hmac = hmac
        self._nonce = nonce
        self._retry = retry

        super().__init__(base_url=base_url, raise_on_unexpected_status=False)

    def with_nonce(self, nonce: str) -> ModulrClient:
        return ModulrClient(self.base_url, self._api_key, self._hmac, nonce=nonce)

    def with_retry(self) -> ModulrClient:
        if self._nonce is None:
            raise ValueError("Cannot set retry without setting nonce")

        return ModulrClient(self.base_url, self._api_key, self._hmac, retry=True)

    def is_retry(self) -> bool:
        return self._retry

    def get_nonce(self) -> str:
        return self._nonce or secrets.token_urlsafe(30)

    def get_date_for_header(self) -> str:
        return format_date_time(datetime.utcnow().timestamp())

    def get_headers(self) -> dict[str, str]:
        now = datetime.now(tz=timezone.utc)
        nonce = self.get_nonce()
        signature_headers = calculate(self._api_key, self._hmac, nonce, now)

        headers = super().get_headers()
        headers.update(signature_headers)  # type: ignore[arg-type]

        if self.is_retry():
            headers["x-mod-retry"] = "true"

        return headers
