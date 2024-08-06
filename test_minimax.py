from board import Board
from agents.minimax_ai import MinimaxAI
from displays import BlankDisplay, GUIDisplay
from main import Game

def start_game(no_gui, max_turn=3):
    board = Board()
    display = BlankDisplay() if no_gui else GUIDisplay(board.board)
    player_1 = MinimaxAI(save_history=True)
    player_2 = MinimaxAI(save_history=True)
    return Game(player_1, player_2, board, display, max_turn)

if __name__ == '__main__':
    game = start_game(True)
    game.run()
    gui = GUIDisplay(game.p1.history[-1][0], framerate=20)
    for board in game.p1.history[-1]:
        gui.set_board(board)
        gui.render()
    gui.terminate()
