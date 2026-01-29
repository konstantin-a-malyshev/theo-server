import logging
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging
from app.db.gremlin import GremlinDB
from app.services.quotation_service import QuotationService
from app.api.routes.health import router as health_router
from app.api.routes.quotations import router as quotations_router

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)

# DB + service singletons
gremlin_db = GremlinDB(settings.GREMLIN_URL, settings.GREMLIN_TRAVERSAL_SOURCE)
quotation_service = QuotationService(gremlin_db)

# Routes
app.include_router(health_router)
app.include_router(quotations_router)


@app.on_event("startup")
def on_startup() -> None:
    gremlin_db.connect()
    logger.info("Server started")


@app.on_event("shutdown")
def on_shutdown() -> None:
    gremlin_db.close()
    logger.info("Server stopped")
