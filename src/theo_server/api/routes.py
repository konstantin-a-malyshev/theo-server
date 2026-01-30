from fastapi import APIRouter, Depends, HTTPException, status

from theo_server.api.schemas import (
    ImportQuotationRequest,
    ImportQuotationResponse,
    MaxImportIndexResponse,
)
from theo_server.security import require_api_key
from theo_server.services.importer import ImportService, QuotationAlreadyExistsError


def get_router(import_service: ImportService) -> APIRouter:
    router = APIRouter(prefix="/v1", tags=["theo"])

    @router.get("/quotations/import-index/max", response_model=MaxImportIndexResponse)
    def max_import_index(_: None = Depends(require_api_key)) -> MaxImportIndexResponse:
        value = import_service.get_max_import_index()
        return MaxImportIndexResponse(maxImportIndex=value)

    @router.post(
        "/quotations/import",
        response_model=ImportQuotationResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def import_quotation(
        body: ImportQuotationRequest,
        _: None = Depends(require_api_key),
    ) -> ImportQuotationResponse:
        try:
            res = import_service.import_quotation(
                caption=body.caption,
                text=body.text,
                book_caption=body.book,
                position=body.position,
                import_index=body.importIndex,
                status=body.status,
            )
        except QuotationAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            ) from e
        return ImportQuotationResponse(**res)

    return router
