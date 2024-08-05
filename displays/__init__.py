from abc import ABC, abstractmethod

class Display(ABC):

    @abstractmethod
    def set_board(self, board):
        ...

    @abstractmethod
    def render(self):
        ...

    @abstractmethod
    def terminate(self):
        ...

class BlankDisplay(Display):

    def set_board(self, board):
        pass

    def render(self):
        pass

    def terminate(self):
        pass

from .gui_display import GUIDisplay