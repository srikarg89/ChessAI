# Pieces: e = empty, p = pawn, r = rook, n = knight, b = bishop, q = queen, k = king
# Uppercase = white, lowercase = black. e is always lowercase

def is_white(piece):
    return piece in 'PRNBQK'

def is_black(piece):
    return piece in 'prnbqk'

def get_empty_board():
    return [['e' for i in range(8)] for j in range(8)]

def get_pos(board, x, y):
    return board[x][y]

def place(board, x, y, piece):
    board[x][y] = piece

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
