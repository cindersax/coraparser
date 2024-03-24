class TableFormatter:
    def __init__(self, strategy: str = "all"):
        """
        Initializes the table formatter with a specified strategy.

        Parameters:
            strategy (str): The strategy to use for formatting tables ('all' is the default strategy,
                            'simple' keeps only the first and last columns).
        """
        self.strategy = strategy

    async def format_tables(self, tables_data):
        """
        Formats extracted tables using the specified strategy.

        Parameters:
            tables_data (list): A list of tables, each table represented as a list of rows.

        Returns:
            list: A list of formatted tables.
        """
        if self.strategy == "simple":
            return await self._format_simple(tables_data)
        elif self.strategy == "all":
            return await self._format_all(tables_data)
        else:
            raise ValueError(f"Unsupported formatting strategy: {self.strategy}")

    async def _format_simple(self, tables_data):
        """
        Formats extracted tables by keeping only the first and last column of each row.

        Parameters:
            tables_data (list): A list of tables, each table represented as a list of rows.

        Returns:
            list: A list of formatted tables, with each row containing only the first and last column.
        """
        formatted_data = []
        for table in tables_data:
            formatted_table = [
                [row[0], row[-1]] if len(row) > 1 else [row[0], row[0]] for row in table
            ]
            formatted_data.append(formatted_table)
        return formatted_data

    async def _format_all(self, tables_data):
        """
        Returns the tables data without any formatting, including all columns.

        Parameters:
            tables_data (list): A list of tables, each table represented as a list of rows.

        Returns:
            list: The same list of tables, unchanged, including all columns.
        """
        # No changes are made to the tables data, so it's returned as is
        return tables_data
