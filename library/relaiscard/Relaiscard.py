from abc import ABC, abstractmethod

class RelaisCard(ABC):

    @abstractmethod
    def set_relais_state(self, channel: int, on: bool = True) -> None:
        pass
    
    def close():
        pass