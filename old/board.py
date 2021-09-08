# Board is an 8x8
# Turn is true if white's turn, False if black's turn
# White's backrank is row 0, black's is row 7

from helpers import *
from pieces import *

class Board:

    def __init__(self):
        self.create_empty_board()


    def create_empty_board(self):
        self.board = [['_' for j in range(8)] for i in range(8)]
        self.white_pieces = [Piece(Color.WHITE)]
        self.black_pieces = [[p[0], 7 - p[1], p[2].upper()] for p in self.white_pieces]
        self.turn = True


    def get_piece_pos(self, pieces, piece_type):
        ret = []
        for piece in self.pieces:
            if piece[2].lower() == piece_type.lower():
                ret.append((piece[0], piece[1]))
        return ret


    # Make sure a given move doesn't put you into check
    def move_valid(self, move: Move):
        # NOTE: Assumes that the current board is valid, and assumes the Move is valid
        my_pieces = self.white_pieces if is_white(move.piece.lower()) else self.black_pieces
        opp_pieces = self.white_pieces if is_black(move.piece.lower()) else self.black_pieces
        if move.specialty is None:
            if move.piece.lower() == 'k':
                # Don't move into check
            else:
                king_pos = self.get_piece_pos(my_pieces, 'k')
                # Don't stop blocking the king from check
        else:
            # TODO: DO THIS
            # Don't castle through check, out of check, or into check
            pass


