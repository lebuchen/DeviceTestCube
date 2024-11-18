from abc import ABC, abstractmethod

class PowerSupply(ABC):
    @abstractmethod
    def set_output_active(self, active: bool) -> None:
        pass

    @abstractmethod
    def set_voltage(self, voltage: float, channel: int = 0) -> None:
        pass

    @abstractmethod
    def set_max_current(self, max_current: float, channel: int = 0) -> None:
        pass
