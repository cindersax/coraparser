from pydantic import BaseModel, HttpUrl
from typing import Literal

class PDFDownloadRequest(BaseModel):
    pdf_url: HttpUrl
    extraction_method: Literal["camelot_stream", "tabula", "camelot_lattice"] = "camelot_stream"
    table_formater: Literal["all", "simple"] = "all"
    output_formater: Literal["json", "csv_single", "csv_multiple"] = "json"
