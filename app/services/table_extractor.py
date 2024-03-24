import camelot
import tabula


class TableExtractor:
    def __init__(self, strategy: str = "camelot"):
        """
        Initializes the table extractor with a specified strategy.

        Parameters:
            strategy (str): The strategy to use for extracting tables ('camelot' or 'tabula').
        """
        self.strategy = strategy

    async def extract(self, pdf_path: str):
        """
        Extracts tables from a PDF file using the specified strategy.

        Parameters:
            pdf_path (str): The file path of the PDF from which to extract tables.

        Returns:
            list: A list of tables extracted from the PDF, each table represented as a list of rows.
        """
        if self.strategy == "camelot":
            return await self._extract_with_camelot(pdf_path)
        elif self.strategy == "tabula":
            return await self._extract_with_tabula(pdf_path)
        else:
            raise ValueError(f"Unsupported extraction strategy: {self.strategy}")

    async def _extract_with_camelot(self, pdf_path: str):
        """Extracts tables using Camelot."""
        tables = camelot.read_pdf(
            pdf_path, pages="all", flavor="stream", row_tol=11.75, strip_text="\n"
        )
        return [table.df.values.tolist() for table in tables]

    async def _extract_with_tabula(self, pdf_path: str):
        """Extracts tables using Tabula."""
        tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
        return [table.values.tolist() for table in tables]
