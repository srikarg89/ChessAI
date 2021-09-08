from helpers import *
from board import Board
from threading import Thread

class Game:
    def __init__(self, display_type):
        self.display = display_type(self)
        self.board = Board()
        self.board.board = get_starting_board()
        self.display.set_board(self.board.board)
        self.display.render()
        self.over = False
        self.turn = Color.WHITE


    def run(self):
        while not self.over:
            self.display.check_action()
            self.display.render()

    def make_move(self, move):
        self.board = self.board.make_move(move)
        self.turn = self.board.turn
        self.display.set_board(self.board.board)
        self.display.render()
