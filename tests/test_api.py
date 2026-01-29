from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# These are smoke tests only; for full tests you'd mock GremlinDB/QuotationService.
def test_routes_exist():
    assert client.get("/quotations/import-index/max").status_code in (200, 500)
