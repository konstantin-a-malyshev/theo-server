from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class MaxImportIndexResponse(BaseModel):
    maxImportIndex: int = Field(..., description="Highest importIndex among quotation vertices (0 if none).")


class ImportQuotationRequest(BaseModel):
    # Book vertex properties
    bookName: str = Field(..., min_length=1)
    bookCaption: str = Field(default="", description="Optional caption for the book vertex.")

    # Quotation vertex properties
    quotationCaption: str = Field(default="")
    text: str = Field(..., min_length=1)
    position: str = Field(default="", description="Position within the e-book (string as provided by your parser).")
    importIndex: int = Field(..., ge=0)


class ImportQuotationResponse(BaseModel):
    created: bool = Field(..., description="True if created; False if a quotation with same importIndex already existed.")
    bookId: str | int
    quotationId: str | int
    importIndex: int
