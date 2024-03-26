import camelot
import tabula

class TableExtractor:
    def __init__(self, strategy: str = "camelot"):
        """
        Initializes the table extractor with a specified strategy.

        Parameters:
            strategy (str): The strategy to use for extracting tables. 
                            Options are 'camelot', 'tabula', or 'camelot-ocr' for OCR support with Camelot.
        """
        self.strategy = strategy

    async def extract(self, pdf_path: str):
        """
        Extracts tables from a PDF file using the specified strategy, optionally using OCR if 'camelot-ocr' is selected.

        Parameters:
            pdf_path (str): The file path of the PDF from which to extract tables.

        Returns:
            list: A list of tables extracted from the PDF, each table represented as a list of rows.

        Raises:
            ValueError: If an unsupported extraction strategy is provided.
            Exception: For errors during the extraction process.
        """
        try:
            if self.strategy == "camelot":
                return await self._extract_with_camelot(pdf_path, use_ocr=False)
            elif self.strategy == "tabula":
                return await self._extract_with_tabula(pdf_path)
            elif self.strategy == "camelot-ocr":
                return await self._extract_with_camelot(pdf_path, use_ocr=True)
            else:
                raise ValueError(f"Unsupported extraction strategy: {self.strategy}")
        except Exception as e:
            # This captures any exception during the table extraction process
            raise Exception(f"Failed to extract tables from PDF: {e}")

    async def _extract_with_camelot(self, pdf_path: str, use_ocr: bool):
        """Extracts tables using Camelot, optionally using OCR."""
        try:
            flavor = "lattice" if use_ocr else "stream"
            tables = camelot.read_pdf(
                pdf_path, pages="all", flavor=flavor, strip_text="\n",
                **({"flag": "--use-ocr"} if use_ocr else {})  # Conditional parameter
            )
            return [table.df.values.tolist() for table in tables]
        except Exception as e:
            raise Exception(f"Camelot{' OCR' if use_ocr else ''} failed to extract tables: {e}")

    async def _extract_with_tabula(self, pdf_path: str):
        """Extracts tables using Tabula."""
        try:
            tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
            return [table.values.tolist() for table in tables]
        except Exception as e:
            raise Exception(f"Tabula failed to extract tables: {e}")
