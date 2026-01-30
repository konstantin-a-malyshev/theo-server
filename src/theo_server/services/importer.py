from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from theo_server.db.gremlin import GremlinClient


class QuotationAlreadyExistsError(Exception):
    def __init__(self, import_index: int) -> None:
        super().__init__(f"Quotation with importIndex={import_index} already exists")
        self.import_index = import_index


@dataclass
class ImportService:
    gremlin: GremlinClient

    def get_max_import_index(self) -> int:
        # Returns -1 if none exist.
        script = """
            def m = g.V().has('type','quotation').values('importIndex').max().tryNext().orElse(null)
            return m == null ? -1 : m
        """.strip()
        res = self.gremlin.submit(script)
        return int(res[0]) if res else -1

    def import_quotation(
        self,
        *,
        caption: str,
        text: str,
        book_caption: str,
        position: str,
        import_index: int,
        status: str,
    ) -> dict[str, Any]:
        # Single Gremlin script so creation + linking happens in one server-side transaction.
        # Returns a map:
        #   { ok: true, quotationId: "...", bookId: "..." }
        # or
        #   { ok: false, reason: "exists" }
        script = """
            def existing = g.V().has('type','quotation').has('importIndex', importIndex).limit(1).hasNext()
            if (existing) {
                return [ok:false, reason:'exists']
            }

            def b = g.V().has('type','book').has('caption', bookCaption)
                .fold()
                .coalesce(
                    unfold(),
                    addV().property('type','book').property('caption', bookCaption).property('name','')
                )
                .next()

            def q = g.addV()
                .property('type','quotation')
                .property('caption', qCaption)
                .property('text', qText)
                .property('book', bookCaption)
                .property('position', qPosition)
                .property('importIndex', importIndex)
                .property('status', qStatus)
                .next()

            b.addEdge('contains', q)

            return [ok:true, quotationId: q.id().toString(), bookId: b.id().toString()]
        """.strip()

        bindings = {
            "qCaption": caption,
            "qText": text,
            "bookCaption": book_caption,
            "qPosition": position,
            "importIndex": int(import_index),
            "qStatus": status,
        }
        res = self.gremlin.submit(script, bindings=bindings)
        if not res:
            raise RuntimeError("Unexpected empty response from Gremlin")
        payload = res[0]
        if isinstance(payload, dict) and payload.get("ok") is False and payload.get("reason") == "exists":
            raise QuotationAlreadyExistsError(import_index)
        if not (isinstance(payload, dict) and payload.get("ok") is True):
            raise RuntimeError(f"Unexpected Gremlin response: {payload!r}")
        return {
            "quotationId": str(payload["quotationId"]),
            "bookId": str(payload["bookId"]),
        }
