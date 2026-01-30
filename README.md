# theo-server

HTTP REST API service for importing *quotation* vertices into a JanusGraph database (via Gremlin Server).

## Features

- API key protection via `X-API-Key` header.
- Get the highest imported quotation index.
- Import a quotation (idempotency by `importIndex`):
  - If a quotation with the same `importIndex` already exists, returns **409 Conflict** and does **not** overwrite.
  - If a book with caption equal to `quotation.book` exists, connects it to the quotation with `contains`.
  - Otherwise creates the book (with empty `name`) and then connects it.

## Data model assumptions

The graph uses vertices with these properties:

- **Book**: `type="book"`, `caption`, `name`
- **Quotation**: `type="quotation"`, `caption`, `text`, `book`, `position`, `importIndex`, `status`

Edge: `contains` from book -> quotation.

The service queries by the `type` property (it does not rely on vertex labels).

> **Tip (recommended for production):** create a unique composite index on `Quotation.importIndex` in JanusGraph to prevent
> race conditions when multiple imports happen concurrently.

## Configuration

Environment variables:

- `THEO_API_KEY` (required): the only accepted API key.
- `GREMLIN_URL` (required): Gremlin Server websocket URL, e.g. `ws://janusgraph:8182/gremlin`
- `THEO_HOST` (optional, default `0.0.0.0`)
- `THEO_PORT` (optional, default `8000`)
- `THEO_LOG_LEVEL` (optional, default `info`)

See `.env.example`.

## Run locally

```bash
python -m venv .venv   // create the virtual environment
.venv/bin/Activate.ps1 // activate the virtual environment, depends on your OS
python -m pip install --upgrade pip
pip install -e .
export THEO_API_KEY="dev-key" // or $env:THEO_API_KEY = "dev-key"
export GREMLIN_URL="ws://localhost:8182/gremlin" // or $env:GREMLIN_URL  = "ws://localhost:8182/gremlin"

uvicorn theo_server.main:app --reload
```

## Run with Docker Compose

1) Copy and edit env file:

```bash
cp .env.example .env
```

2) Start:

```bash
docker compose up --build
```

The API will be available at:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## API

All endpoints require header:

- `X-API-Key: <your key>`

### Get highest import index

`GET /v1/quotations/import-index/max`

Response:

```json
{ "maxImportIndex": 123 }
```

If there are no quotations yet, returns `-1`.

### Import quotation

`POST /v1/quotations/import`

Body:

```json
{
  "caption": "Some title",
  "text": "Quote text",
  "book": "Book caption",
  "position": "loc:1234",
  "importIndex": 42,
  "status": "new"
}
```

Responses:

- `201 Created` with ids:
  ```json
  { "quotationId": "...", "bookId": "..." }
  ```
- `409 Conflict` if `importIndex` already exists.

## License

MIT (you can change as needed).
