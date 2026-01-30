from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from gremlin_python.driver.client import Client
from gremlin_python.driver.serializer import GraphSONSerializersV3d0
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class GremlinClient:
    url: str
    traversal_source: str = "g"

    def __post_init__(self) -> None:
        # GraphSON 3.0 works well with JanusGraph + TinkerPop 3.x
        self._client = Client(
            self.url,
            self.traversal_source,
            message_serializer=GraphSONSerializersV3d0(),
        )

    def close(self) -> None:
        self._client.close()

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=0.5, min=0.5, max=5))
    def submit(self, script: str, bindings: Mapping[str, Any] | None = None) -> list[Any]:
        result_set = self._client.submit(script, bindings=bindings or {})
        return result_set.all().result()
