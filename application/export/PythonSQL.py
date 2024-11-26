from .Export import Export

class PythonSQl(Export):
    def _export_to_database(self, report_name: str, report_table: list) -> None:
        # Connect to SQLite database
        print(report_name)
        print(report_table)
        pass