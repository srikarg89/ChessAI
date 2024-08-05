from board import Board
from agents.minimax_ai import MinimaxAI
from agents.human import Human
from displays import BlankDisplay, GUIDisplay
from base import Color

class Game:
    def __init__(self, p1, p2, board, display, max_turns):
        self.p1, self.p2 = p1, p2
        self.board = board
        self.display = display
        self.display.set_board(self.board.board)
        self.display.render()
        self.over = False
        self.max_turns = max_turns


    def run(self):
        for _ in range(self.max_turns):
            if self.over:
                break
            player = self.p1 if self.board.turn == Color.WHITE else self.p2
            move = player.get_move(self.board)
            if move is not None:
                self.board = self.board.make_move(move)
                self.display.set_board(self.board.board)
            self.display.render()
            
        self.display.terminate()


def start_game(player_1_type, player_2_type, no_gui, max_turn=300):
    if player_1_type == 'Human' and no_gui:
        raise ValueError("Cannot play without GUI if player 1 is Human")
    if player_2_type == 'Human' and no_gui:
        raise ValueError("Cannot play without GUI if player 2 is Human")

    board = Board()
    display = BlankDisplay() if no_gui else GUIDisplay(board.board)
    player_1 = Human(display) if player_1_type == 'Human' else MinimaxAI()
    player_2 = Human(display) if player_2_type == 'Human' else MinimaxAI()
    return Game(player_1, player_2, board, display, max_turn)

# TODO: Ask for piece to promote to if promotion (human version)

if __name__ == '__main__':
    game = start_game('Human', 'AI', False, 400)
    game.run()
