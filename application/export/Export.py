from abc import ABC, abstractmethod

class Export(ABC):
    @abstractmethod
    def export_to_database(report_name: str, report_table: list) -> None:
        pass