from fastapi import FastAPI

from theo_server.config import settings
from theo_server.db.gremlin import GremlinClient
from theo_server.api.routes import get_router
from theo_server.services.importer import ImportService


def create_app() -> FastAPI:
    app = FastAPI(title="theo-server", version="0.1.0")

    gremlin = GremlinClient(settings.gremlin_url)
    import_service = ImportService(gremlin=gremlin)

    @app.on_event("shutdown")
    def _shutdown() -> None:
        gremlin.close()

    @app.get("/healthz", tags=["health"])
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(get_router(import_service))
    return app


app = create_app()
