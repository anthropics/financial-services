"""A small, dependency-free HTTP client for SEC EDGAR.

Everything that talks to SEC goes through here, so the two fair-access rules are
enforced in one place for the whole connector:

1. A descriptive **User-Agent** header on every request (SEC requires this).
2. Throttling to stay **well under 10 requests/second**.

It also retries on transient errors and transparently handles gzip. It uses only
the Python standard library (urllib) so the connector stays lightweight and easy
to install — no third-party HTTP dependency to break on new Python versions.
"""
from __future__ import annotations

import gzip
import json
import time
import urllib.error
import urllib.request
from typing import Any, BinaryIO


class SecHttpClient:
    """Compliant gateway to SEC EDGAR over HTTP."""

    def __init__(
        self,
        user_agent: str,
        min_interval: float = 0.15,
        timeout: float = 60.0,
        max_retries: int = 4,
    ) -> None:
        self.user_agent = user_agent
        self.min_interval = min_interval  # seconds between requests
        self.timeout = timeout
        self.max_retries = max_retries
        self._last_request = 0.0

    # -- internals ------------------------------------------------------------
    def _headers(self) -> dict[str, str]:
        return {"User-Agent": self.user_agent, "Accept-Encoding": "gzip"}

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_request = time.monotonic()

    def _open(self, url: str) -> BinaryIO:
        """Open a readable, decompressed stream for `url`, with retries/back-off."""
        last_err: Exception | None = None
        for attempt in range(self.max_retries):
            self._throttle()
            req = urllib.request.Request(url, headers=self._headers())
            try:
                resp = urllib.request.urlopen(req, timeout=self.timeout)
                if resp.headers.get("Content-Encoding") == "gzip":
                    return gzip.GzipFile(fileobj=resp)  # type: ignore[return-value]
                return resp  # type: ignore[return-value]
            except urllib.error.HTTPError as e:
                last_err = e
                # Retry only on rate-limit / transient server errors.
                if e.code in (429, 500, 502, 503, 504):
                    time.sleep(min(2 ** attempt, 10))
                    continue
                raise
            except urllib.error.URLError as e:
                last_err = e
                time.sleep(min(2 ** attempt, 10))
        raise RuntimeError(
            f"SEC request failed after {self.max_retries} attempts: {url} ({last_err})"
        )

    # -- public API -----------------------------------------------------------
    def get_bytes(self, url: str) -> bytes:
        with self._open(url) as stream:
            return stream.read()

    def get_text(self, url: str, encoding: str = "utf-8") -> str:
        return self.get_bytes(url).decode(encoding, errors="replace")

    def get_json(self, url: str) -> Any:
        return json.loads(self.get_bytes(url))

    def open_stream(self, url: str) -> BinaryIO:
        """Open a streaming handle suitable for incremental XML parsing.

        Used for the very large ABS-EE loan-level files (tens to >100 MB): the
        caller feeds this straight into xml.etree.ElementTree.iterparse so the
        file is processed record-by-record and never fully held in memory.
        The caller is responsible for closing the returned handle.
        """
        return self._open(url)
