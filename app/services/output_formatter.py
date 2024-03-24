import csv
import json
import os
from datetime import datetime


class OutputFormatter:
    def __init__(self, output_dir: str, file_type: str = "json"):
        """
        Initializes the output formatter with a directory to save files and the output format type.

        Parameters:
            output_dir (str): The directory where output files will be saved.
            file_type (str): The type of file to create ('json', 'csv_single', 'csv_multiple', etc.).
        """
        self.output_dir = output_dir
        self.file_type = file_type
        os.makedirs(output_dir, exist_ok=True)

    async def format_to_file(self, data):
        """
        Formats and writes data to a file of the specified type, auto-generating the filename.

        Parameters:
            data: The data to be written to the file.

        Returns:
            str or list: The path(s) to the created file(s).
        """
        filename = self._generate_filename()
        if self.file_type == "json":
            return await self._write_json(data, filename)
        elif self.file_type == "csv_single":
            return await self._write_csv_single(data, filename)
        elif self.file_type == "csv_multiple":
            return await self._write_csv_multiple(data, filename)
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

    def _generate_filename(self):
        """
        Generates a filename based on the current timestamp and the file type.

        Returns:
            str: The generated base filename without the file extension.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"output_{timestamp}"

    async def _write_json(self, data, filename: str):
        path = os.path.join(self.output_dir, f"{filename}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return [path]

    async def _write_csv_single(self, data, filename: str):
        path = os.path.join(self.output_dir, f"{filename}.csv")
        await self._write_to_csv(path, data, separate_tables=True)
        return [path]

    async def _write_csv_multiple(self, data, filename: str):
        paths = []
        for i, table in enumerate(data, start=1):
            table_filename = f"{filename}_table_{i}"
            path = os.path.join(self.output_dir, table_filename + ".csv")
            await self._write_to_csv(path, [table], separate_tables=False)
            paths.append(path)
        return paths

    async def _write_to_csv(self, filepath, data, separate_tables=False):
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for table in data:
                writer.writerows(table)
                if separate_tables:
                    writer.writerow([])
