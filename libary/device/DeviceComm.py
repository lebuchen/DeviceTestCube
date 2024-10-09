from abc import ABC, abstractmethod
from typing import List

class devicecomm(ABC):

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

    @abstractmethod
    def get_event(
        self, master: int = None, port: int = None
        ) -> any:
            pass