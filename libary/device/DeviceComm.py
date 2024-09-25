from abc import ABC, abstractmethod
from typing import List

class devicecomm(ABC):

    @abstractmethod
    def get_processdata_value(self, master: int = None, port: int = None) -> any:
        pass

    @abstractmethod
    def post_processdata_value(
        self,
        iq_value: bool = None,
        cq_value: bool = None,
        io_link_value: List[int] = None,
        io_link_valid: bool = True,
        master: int = None,
        port: int = None,
    ) -> None:
        pass

    @abstractmethod
    def get_processdata_getdata_value(
        self, master: int = None, port: int = None
    ) -> any:
        pass

    @abstractmethod
    def get_processdata_setdata_value(
        self, master: int = None, port: int = None
    ) -> any:
        pass
