import logging
from typing import Any, Dict, Optional

from gremlin_python.driver.client import Client

logger = logging.getLogger(__name__)


class GremlinDB:
    """
    Thin wrapper around gremlinpython Client.
    Uses script submissions with bindings to keep traversals parameterized.
    """

    def __init__(self, url: str, traversal_source: str):
        self._url = url
        self._ts = traversal_source
        self._client: Optional[Client] = None

    def connect(self) -> None:
        if self._client is None:
            logger.info("Connecting to Gremlin Server: %s (source=%s)", self._url, self._ts)
            self._client = Client(self._url, self._ts)

    def close(self) -> None:
        if self._client is not None:
            logger.info("Closing Gremlin client")
            self._client.close()
            self._client = None

    def submit_one(self, script: str, bindings: Optional[Dict[str, Any]] = None) -> Any:
        """
        Submit a Gremlin script and return the first item (or None).
        """
        if self._client is None:
            raise RuntimeError("GremlinDB is not connected. Call connect() first.")

        res = self._client.submit(script, bindings or {})
        items = res.all().result()
        return items[0] if items else None

    def submit_all(self, script: str, bindings: Optional[Dict[str, Any]] = None) -> list[Any]:
        if self._client is None:
            raise RuntimeError("GremlinDB is not connected. Call connect() first.")

        res = self._client.submit(script, bindings or {})
        return res.all().result()
