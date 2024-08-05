from . import Agent

class Human(Agent):
    def __init__(self, display):
        self.display = display

    # TODO: Ask for piece to promote to if promotion (human version)
    def get_move(self, board):
        return self.display.check_ui_action(board.turn)
