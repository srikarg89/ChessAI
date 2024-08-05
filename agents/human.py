from . import Agent

class Human(Agent):
    def __init__(self, display):
        self.display = display

    def get_move(self, board):
        return self.display.check_ui_action(board.turn)
