# Pieces: e = empty, p = pawn, r = rook, n = knight, b = bishop, q = queen, k = king
# Uppercase = white, lowercase = black. e is always lowercase

from enum import IntEnum
# TODO: Use dataclasses?
class Move:
    # Specialties: O-O, O-O-O, EP (en pessant), pQ, pN, pB, pR (promotion into queen, knight, bishop, or rook respectively)
    def __init__(self, prev_pos, new_pos, piece, specialty=None):
        self.prev_pos = prev_pos
        self.new_pos = new_pos
        self.piece = piece
        self.specialty = specialty
    
    def __str__(self):
        return "Move[piece {} on {} to {} with specialty {}]".format(self.piece, str(self.prev_pos), str(self.new_pos), str(self.specialty))
    
    def copy(self):
        return Move(self.prev_pos, self.new_pos, self.piece, self.specialty)
    

class Color(IntEnum):
    WHITE = 0
    BLACK = 1

    def opp(self):
        return Color.WHITE if self == Color.BLACK else Color.BLACK

PIECE_VALUE = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 10000}
BLACK_PIECES = {*'prnbqk'}
WHITE_PIECES = {*'PRNBQK'}

def in_bounds(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

def is_white(piece):
    return piece in WHITE_PIECES

def is_black(piece):
    return piece in BLACK_PIECES

def move_in_arr(move, arr):
    for val in arr:
        if val.prev_pos == move.prev_pos and val.new_pos == move.new_pos and val.piece == move.piece:
            return val
    return None

def get_captured_pos(board, move: Move):
    # Check for any special functionality
    if move.specialty == 'EP':
        return (move.new_pos[0], move.prev_pos[1])

    return None if board[move.new_pos[0]][move.new_pos[1]] == 'e' else move.new_pos

def make_piece(color, piece):
    return piece.upper() if color == Color.WHITE else piece.lower()

# Transposes a given 2D matrix
def transpose(matrix):
    t = []
    for i in range(len(matrix[0])): 
        t.append([])
        for j in range(len(matrix)):
            t[-1].append(matrix[j][i])
    return t
