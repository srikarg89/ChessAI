from helpers import *
from threading import Thread

class Game:
    def __init__(self, display_type):
        self.display = display_type(self)
        self.board = get_starting_board()
        self.display.set_board(self.board)
        self.display.render()
        self.over = False
        self.turn = True # True = white's turn, False = black's turn
        self.pieces = []

    def run(self):
        while not self.over:
            self.display.check_action()
            self.display.render()
    
    def check_wall(self, x, y):
        return x < 0 or y < 0 or x >= 8 or y >= 8

    def check_ally_present(self, x, y, piece):
        if self.check_wall(x, y):
            return False
        target = get_pos(self.board, x, y)
        return (is_white(piece) and is_white(target)) or (is_black(piece) and is_black(target))

    def check_enemy_present(self, x, y, piece):
        if self.check_wall(x, y):
            return False
        target = get_pos(self.board, x, y)
        return (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target))

    def get_possible_moves_loop(self, piece, x, y, dx, dy, poss):
        for d in range(1, 9):
            if self.check_wall(x + d*dx, y + d*dy) or self.check_ally_present(x + d*dx, y + d*dy, piece):
                break
            poss.append((x + d*dx, y + d*dy))
            if self.check_enemy_present(x + d*dx, y + d*dy, piece):
                break

    def get_possible_moves(self, x, y, piece):
        backrank = 0 if piece == piece.upper() else 7
        direction = 1 if piece == piece.upper() else -1
        poss = []
        if piece.lower() == 'k':
            # Loop through king moves
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    # Move one square in any direction
                    if self.check_wall(x + dx, y + dy) or self.check_ally_present(x + dx, y + dy, piece):
                        continue
                    poss.append((x + dx, y + dy))
                    # TODO: Check if you're walking into a check

        if piece.lower() == 'r' or piece.lower() == 'q':
            # Check horizontal / vertical motion (rook / queen moves)
            self.get_possible_moves_loop(piece, x, y, 1, 0, poss)
            self.get_possible_moves_loop(piece, x, y, -1, 0, poss)
            self.get_possible_moves_loop(piece, x, y, 0, 1, poss)
            self.get_possible_moves_loop(piece, x, y, 0, -1, poss)

        if piece.lower() == 'b' or piece.lower() == 'q':
            # Check diagonals (bishop / queen moves)
            self.get_possible_moves_loop(piece, x, y, 1, 1, poss)
            self.get_possible_moves_loop(piece, x, y, 1, -1, poss)
            self.get_possible_moves_loop(piece, x, y, -1, 1, poss)
            self.get_possible_moves_loop(piece, x, y, -1, -1, poss)

        if piece.lower() == 'n':
            # Loop through possible knight moves
            for dx in [-2, -1, 1, 2]:
                for dy in [-2, -1, 1, 2]:
                    if abs(dx) == abs(dy):
                        continue
                    if self.check_wall(x + dx, y + dy) or self.check_ally_present(x + dx, y + dy, piece):
                        continue
                    poss.append((x + dx, y + dy))

        if piece.lower() == 'p':
            # Pawn moves
            # Forward moves
            if not self.check_wall(x, y + direction) and get_pos(self.board, x, y + direction * 1) == 'e':
                poss.append((x, y + direction))
                if y == backrank + direction and get_pos(self.board, x, y + direction * 2) == 'e': # Hasn't moved (still on the second rank)
                    poss.append((x, y + direction * 2))
            # Diagonal captures
            targets = [(x + dx, y + direction) for dx in [-1, 1]]
            for target in targets:
                if self.check_enemy_present(target[0], target[1], piece):
                    poss.append(target)

        # TODO: Add castling
        # TODO: Add en pessant
        # TODO: Add promotion
        return poss

    
    def make_move(self, x, y, targetX, targetY, piece):
        if is_white(piece) and not self.turn:
            return
        if is_black(piece) and self.turn:
            return
        poss = self.get_possible_moves(x, y, piece)
        if (targetX, targetY) in poss: # Made a move
            place(self.board, targetX, targetY, piece)
            self.turn = not self.turn
        else:
            place(self.board, x, y, piece)



