# Pieces: e = empty, p = pawn, r = rook, n = knight, b = bishop, q = queen, k = king
# Uppercase = white, lowercase = black. e is always lowercase

from enum import Enum
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
    

class Color(Enum):
    WHITE = True
    BLACK = False

    def opp(self):
        return Color.WHITE if self == Color.BLACK else Color.BLACK


ALL_COLORS = [Color.WHITE, Color.BLACK]
MOVEMENT = {Color.WHITE: 1, Color.BLACK: -1}
STARTRANK = {Color.WHITE: 0, Color.BLACK: 7}
ENDRANK = {Color.WHITE: 7, Color.BLACK: 0}
PIECE_VALUE = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 10000}

def in_bounds(pos):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < 8 and pos[1] < 8

def in_bounds2(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

def is_white(piece):
    return piece in 'PRNBQK'

def is_black(piece):
    return piece in 'prnbqk'

def move_in_arr(move, arr):
    for val in arr:
        if val.prev_pos == move.prev_pos and val.new_pos == move.new_pos and val.piece == move.piece:
            return val
    return None
