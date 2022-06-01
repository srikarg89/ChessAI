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
    

ALL_COLORS = [Color.WHITE, Color.BLACK]
MOVEMENT = {Color.WHITE: 1, Color.BLACK: -1}
STARTRANK = {Color.WHITE: 0, Color.BLACK: 7}
ENDRANK = {Color.WHITE: 7, Color.BLACK: 0}
PIECE_VALUE = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 10000}

def opp_color(color):
    return Color.WHITE if color == Color.BLACK else Color.BLACK

def in_bounds(pos):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < 8 and pos[1] < 8

def in_bounds2(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

def is_white(piece):
    return piece in 'PRNBQK'

def is_black(piece):
    return piece in 'prnbqk'

# Transposes a given 2x2 matrix
def transpose(matrix):
    t = []
    for i in range(len(matrix[0])): 
        t.append([])
        for j in range(len(matrix)):
            t[-1].append(matrix[j][i])
    return t

# Transposes the board to make the printed output easier to read
def printboard(board):
    print('\n'.join([''.join(row) for row in transpose(board)]))

def make_piece(color, piece):
    return piece.upper() if color == Color.WHITE else piece.lower()

# Place pieces in starting configuration
def get_starting_board():
    board = [['e' for i in range(8)] for j in range(8)]
    backrank_order = "rnbqkbnr"
    for x in range(8):
        board[x][0] = backrank_order[x].upper()
        board[x][1] = 'P'
        board[x][6] = 'p'
        board[x][7] = backrank_order[x]
    return board

def get_filename(piece):
    if piece == 'e':
        return None
    img_map = {'r': 'rook', 'n': 'knight', 'b': 'bishop', 'p': 'pawn', 'q': 'queen', 'k': 'king'}
    filename = 'images/' + ('b' if piece == piece.lower() else 'w') + img_map[piece.lower()] + '.png'
    return filename

def list_replace(arr, ori, new):
    for i in range(len(arr)):
        if arr[i] == ori:
            arr[i] = new
    return arr

def move_in_arr(move, arr):
    for val in arr:
        if val.prev_pos == move.prev_pos and val.new_pos == move.new_pos and val.piece == move.piece:
            return val
    return None

def heuristic(board, piece_list):
    score = 0
    value_dict = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 10000}
    for loc in piece_list:
        typ = board[loc[0]][loc[1]].lower()
        score += value_dict[typ]
    return score
