from fastapi import FastAPI, HTTPException
from .models import PDFDownloadRequest
from .services.pdf_downloader import PDFDownloader
from .services.table_extractor import TableExtractor
from .services.table_formatter import TableFormatter
from .services.output_formatter import OutputFormatter
import os


app = FastAPI(
    title="PDF Table Extractor API",
    description="This API extracts tables from PDF documents, formats them, and saves the results to a specified file format. It supports multiple table extraction methods and output formats.",
    version="1.0.0",
)

TABLES_DIR = "extracted_tables"
os.makedirs(TABLES_DIR, exist_ok=True)


@app.post(
    "/extract-tables/",
    response_model=dict,
    tags=["Extraction Operations"],
    summary="Extract and format tables from a PDF document",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Tables extracted and formatted successfully.",
                        "files": [
                            "extracted_tables/output_20231015T153000_table_1.csv",
                            "extracted_tables/output_20231015T153000_table_2.csv",
                        ],
                    }
                }
            },
        },
        400: {"description": "Invalid Request"},
        500: {"description": "Extraction Error"},
    },
)
async def extract_tables(request: PDFDownloadRequest):
    """
    Extracts tables from a PDF document based on the URL and extraction method provided in the request.
    The extracted tables are then formatted and saved to a file in a specified format.

    - **pdf_url**: The URL of the PDF from which to extract tables.
    - **extraction_method**: The method to use for table extraction ('camelot' or 'tabula').

    The endpoint dynamically handles the process of downloading the PDF, extracting tables,
    formatting the extracted data, and saving the formatted data to files.
    """

    pdf_downloader = PDFDownloader(strategy="httpx")
    table_extractor = TableExtractor(strategy=request.extraction_method)
    table_formatter = TableFormatter(strategy="simple")
    output_formatter = OutputFormatter(output_dir=TABLES_DIR, file_type="json")

    pdf_path = None
    try:
        pdf_path = await pdf_downloader.download(request.pdf_url)
        tables_data = await table_extractor.extract(pdf_path)
        formatted_tables_data = await table_formatter.format_tables(tables_data)
        file_paths = await output_formatter.format_to_file(formatted_tables_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)

    return {
        "message": "Tables extracted and formatted successfully.",
        "files": file_paths,
    }
