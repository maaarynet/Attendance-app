from abc import ABC, abstractmethod

class ScreenInterface(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass
