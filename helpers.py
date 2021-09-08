# Pieces: e = empty, p = pawn, r = rook, n = knight, b = bishop, q = queen, k = king
# Uppercase = white, lowercase = black. e is always lowercase

from enum import Enum
class Move:
    # Specialties: O-O, O-O-O, EP (en pessant), promotion_Q, promotion_N, promotion_B, promotion_R
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
    

def opp_color(color):
    return Color.WHITE if color == Color.BLACK else Color.BLACK

def add(pos, pos1):
    return (pos[0] + pos1[0], pos[1] + pos1[1])

def in_bounds(pos):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < 8 and pos[1] < 8

def is_white(piece):
    return piece in 'PRNBQK'

def is_black(piece):
    return piece in 'prnbqk'

def get_direction(color):
    return 1 if color == Color.WHITE else -1

def get_empty_board():
    return [['e' for i in range(8)] for j in range(8)]

def get_pos(board, x, y):
    return board[x][y]

def place(board, x, y, piece):
    board[x][y] = piece

def make_piece(color, piece):
    if color == Color.WHITE:
        return piece.upper()
    return piece.lower()

def get_starting_board():
    board = get_empty_board()
    # Place starting pieces
    backrank_order = [*"rnbqkbnr"]
    # Place pawns
    for x in range(8):
        place(board, x, 0, backrank_order[x].upper())
        place(board, x, 1, 'P')
        place(board, x, 6, 'p')
        place(board, x, 7, backrank_order[x])
    return board

def get_filename(piece):
    if piece == 'e':
        return None
    img_map = {'r': 'rook', 'n': 'knight', 'b': 'bishop', 'p': 'pawn', 'q': 'queen', 'k': 'king'}
    filename = 'images/' + ('b' if piece == piece.lower() else 'w') + img_map[piece.lower()] + '.png'
    return filename


def move_in_arr(move, arr):
    for val in arr:
        if val.prev_pos == move.prev_pos and val.new_pos == move.new_pos and val.piece == move.piece:
            return val
    return None
        
