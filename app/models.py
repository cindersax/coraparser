from pydantic import BaseModel, HttpUrl


class PDFDownloadRequest(BaseModel):
    pdf_url: HttpUrl
    extraction_method: str = "camelot"
