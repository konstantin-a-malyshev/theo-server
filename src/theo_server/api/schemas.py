from pydantic import BaseModel, Field


class MaxImportIndexResponse(BaseModel):
    maxImportIndex: int = Field(..., description="Highest importIndex found, or -1 if none.")


class ImportQuotationRequest(BaseModel):
    caption: str
    text: str
    book: str = Field(..., description="Book caption.")
    position: str
    importIndex: int
    status: str


class ImportQuotationResponse(BaseModel):
    quotationId: str
    bookId: str
