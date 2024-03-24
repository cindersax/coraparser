import httpx
import tempfile


class PDFDownloader:
    def __init__(self, strategy: str = "httpx"):
        """
        Initializes the PDF downloader with a specified strategy.

        Parameters:
            strategy (str): The strategy to use for downloading PDFs ('httpx' is the default and only strategy for now).
        """
        self.strategy = strategy

    async def download(self, url: str):
        """
        Downloads a PDF from a URL using the specified strategy.

        Parameters:
            url (str): The URL of the PDF to download.

        Returns:
            str: The file path to the downloaded PDF.

        Raises:
            ValueError: If the URL does not point to a PDF file or if an unsupported strategy is provided.
        """
        if self.strategy == "httpx":
            return await self._download_with_httpx(url)
        else:
            raise ValueError(f"Unsupported download strategy: {self.strategy}")

    async def _download_with_httpx(self, url: str):
        """Downloads a PDF using the httpx library."""
        url_str = str(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url_str)
        if response.headers.get("Content-Type", "") != "application/pdf":
            raise ValueError("URL does not point to a PDF file")
        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        with pdf_file as f:
            f.write(response.content)
        return pdf_file.name
