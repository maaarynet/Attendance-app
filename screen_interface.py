from abc import ABC, abstractmethod

class ScreenInterface(ABC):
    @abstractmethod
    def display(self):
        """Отображает экран."""
        pass

    @abstractmethod
    def handle_event(self, event):
        """Обрабатывает события (нажатие клавиш, клики)."""
        pass
