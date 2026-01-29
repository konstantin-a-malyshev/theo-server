from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import (
    ImportQuotationRequest,
    ImportQuotationResponse,
    MaxImportIndexResponse,
)
from app.services.quotation_service import QuotationService

router = APIRouter(prefix="/quotations", tags=["quotations"])


def get_service() -> QuotationService:
    # late import to avoid circulars
    from app.main import quotation_service
    return quotation_service


@router.get("/import-index/max", response_model=MaxImportIndexResponse)
def get_max_import_index(service: QuotationService = Depends(get_service)) -> MaxImportIndexResponse:
    try:
        mx = service.get_max_import_index()
        return MaxImportIndexResponse(maxImportIndex=mx)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import", response_model=ImportQuotationResponse)
def import_quotation(
    req: ImportQuotationRequest,
    service: QuotationService = Depends(get_service),
) -> ImportQuotationResponse:
    try:
        result = service.import_quotation(req.model_dump())
        return ImportQuotationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
