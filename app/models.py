from pydantic import BaseModel, HttpUrl


class PDFDownloadRequest(BaseModel):
    pdf_url: HttpUrl
    extraction_method: str = "camelot"
    table_formater: str = "all"
    output_formater: str = "json"
    
    
