# theo-server

## Data model

Vertices:
- book: `caption` (string), `name` (string)
- quotation: `caption` (string), `text` (string), `book` (string), `position` (string), `importIndex` (int)

Edges:
- `contains`: book -> quotation

## API

### Health
GET `/health`

### Get highest importIndex
GET `/quotations/import-index/max`

Response:
```json
{ "maxImportIndex": 123 }
```

### Import a quotation (idempotent by importIndex)
POST `/quotations/import`

Request:
```json
{
  "bookName": "The Great Book",
  "bookCaption": "Optional caption",
  "quotationCaption": "Optional caption",
  "text": "Some quotation text",
  "position": "epubcfi(/6/2[chapter1]!/4/1:0)",
  "importIndex": 124
}
```

Response:
```json
{
  "created": true,
  "bookId": "1234",
  "quotationId": "5678",
  "importIndex": 124
}
```

If the same `importIndex` already exists, it returns `created=false` and the existing quotation id.

## Run locally (Docker)

1. Copy env:
   - `cp .env.example .env`

2. Start:
   - `docker compose up --build`

3. Try:
   - `curl http://localhost:8000/health`
   - `curl http://localhost:8000/quotations/import-index/max`

## Notes / production tips

- Create a composite index on `quotation.importIndex` and `book.name` in JanusGraph for speed/uniqueness.
- The compose file uses an in-memory JanusGraph config for development convenience.
  For production, point `GREMLIN_URL` to your actual Gremlin Server and remove the `janusgraph` service.
