from board import Board
from minimax_ai import AI
from display import GUIDisplay
from helpers import Color, printboard

class Game:
    def __init__(self, p1_type, p2_type, display_type, max_turns):
        self.p1 = 'Human' if p1_type == 'Human' else AI()
        self.p2 = 'Human' if p2_type == 'Human' else AI()
        self.board = Board()
        if True:
            self.display = display_type(self.board.board)
            self.display.set_board(self.board.board)
            self.display.render()
        self.over = False
        self.max_turns = max_turns


    def run(self):
        for i in range(self.max_turns):
            if self.over:
                break
            player = self.p1 if self.board.turn == Color.WHITE else self.p2
            if player == 'Human':
                action = self.display.check_ui_action(self.board.turn)
                if action is not None:
                    print("MAKING MOVE: ", action)
                    self.make_move(action)
                self.display.render()
            else: # AI
                action = player.get_move(self.board)
                self.make_move(action)
        self.display.terminate()


    def make_move(self, move):
        self.board = self.board.make_move(move)
        self.display.set_board(self.board.board)
        self.display.render()

# TODO: Ask for piece to promote to if promotion (human version)

if __name__ == '__main__':
    g = Game('Human', 'AI', GUIDisplay, 10000)
    # g = Game('AI', 'AI', GUIDisplay, float("inf"))
    # g = Game('AI', 'AI', GUIDisplay, 10)
    g.run()
