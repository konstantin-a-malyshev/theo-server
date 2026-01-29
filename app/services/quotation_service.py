import logging
from typing import Any, Dict

from app.db.gremlin import GremlinDB

logger = logging.getLogger(__name__)


class QuotationService:
    def __init__(self, db: GremlinDB):
        self.db = db

    def get_max_import_index(self) -> int:
        """
        Returns 0 if no quotation vertices exist or importIndex is missing everywhere.
        """
        script = """
        g.V().hasLabel('quotation').has('importIndex').
          order().by('importIndex', decr).
          limit(1).values('importIndex').fold().
          coalesce(unfold(), constant(0))
        """
        val = self.db.submit_one(script)
        try:
            return int(val)
        except Exception:
            return 0

    def import_quotation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Idempotent by importIndex:
        - If quotation with same importIndex exists: returns created=False + existing ids
        - Else: upserts book, creates quotation, creates contains edge, returns created=True + ids
        """
        script = """
        // 1) Check if quotation already exists by importIndex
        existingQ = g.V().hasLabel('quotation').has('importIndex', importIndex).limit(1).fold().
            coalesce(unfold(), constant(null)).next()

        // 2) Upsert book by name
        b = g.V().hasLabel('book').has('name', bookName).fold().
            coalesce(
              unfold(),
              addV('book').property('name', bookName).property('caption', bookCaption)
            ).next()

        if (existingQ != null) {
            // Ensure edge exists (optional; we create it if missing)
            hasEdge = g.V(b).outE('contains').inV().hasId(existingQ.id()).limit(1).hasNext()
            if (!hasEdge) {
                g.V(b).addE('contains').to(g.V(existingQ)).iterate()
            }
            return [created:false, bookId:b.id(), quotationId:existingQ.id(), importIndex:importIndex]
        }

        // 3) Create quotation
        q = g.addV('quotation').
            property('caption', quotationCaption).
            property('text', qText).
            property('book', bookName).
            property('position', qPosition).
            property('importIndex', importIndex).
            next()

        // 4) Link book -> quotation via 'contains'
        g.V(b).addE('contains').to(g.V(q)).iterate()

        return [created:true, bookId:b.id(), quotationId:q.id(), importIndex:importIndex]
        """
        bindings = {
            "bookName": payload["bookName"],
            "bookCaption": payload.get("bookCaption", "") or "",
            "quotationCaption": payload.get("quotationCaption", "") or "",
            "qText": payload["text"],
            "qPosition": payload.get("position", "") or "",
            "importIndex": int(payload["importIndex"]),
        }

        result = self.db.submit_one(script, bindings)
        if not isinstance(result, dict):
            raise RuntimeError(f"Unexpected Gremlin response: {result!r}")

        return result
