from base import is_white, is_black, Color, in_bounds, Move, get_captured_pos, make_piece

def find_piece(board, piece):
    locs = []
    for x in range(8):
        for y in range(8):
            char = board[x][y]
            if char == piece:
                locs.append((x,y))
    return locs

class Player:
    def __init__(self, color, board, run_constructor=True):
        self.color = color
        self.forwards_movement = 1 if self.color == Color.WHITE else -1
        self.startrank = 0 if self.color == Color.WHITE else 7
        self.endrank = 7 if self.color == Color.WHITE else 0
        if run_constructor:
            self.king_has_moved = False
            self.lrook_has_moved = False
            self.rrook_has_moved = False

            self.pieces = self.get_all_pieces(board)
            self.king_pos = find_piece(board, make_piece(self.color, 'k'))[0]

    def make_copy(self, board) -> "Player":
        new_player = Player(self.color, board, run_constructor=False)

        new_player.king_has_moved = self.king_has_moved
        new_player.lrook_has_moved = self.lrook_has_moved
        new_player.rrook_has_moved = self.rrook_has_moved

        new_player.pieces = self.pieces.copy()
        new_player.king_pos = self.king_pos

        return new_player

    def get_all_pieces(self, board):
        pieces = set()
        color_check = is_white if self.color == Color.WHITE else is_black
        for x in range(8):
            for y in range(8):
                char = board[x][y]
                if color_check(char):
                    pieces.add((x,y))
        return pieces

    def remove_piece(self, loc):
        self.pieces.remove(loc)

    def add_piece(self, loc):
        self.pieces.add(loc)

    def move_piece(self, before, after):
        self.pieces.remove(before)
        self.pieces.add(after)

    def get_vision_loop(self, board, x, y, dx, dy):
        vision = set()
        for d in range(1, 9):
            if not in_bounds(x + d*dx, y + d*dy):
                break
            vision.add((x + d*dx, y + d*dy))
            if board[x + d*dx][y + d*dy] != 'e':
                # We can see this piece, but we can't see past this piece.
                vision.add((x + d*dx, y + d*dy))
                break
        return vision

    def king_vision(self, x, y):
        vision = set()
        if in_bounds(x - 1, y - 1):
            vision.add((x - 1, y - 1))
        if in_bounds(x - 1, y):
            vision.add((x - 1, y))
        if in_bounds(x - 1, y + 1):
            vision.add((x - 1, y + 1))
        if in_bounds(x, y - 1):
            vision.add((x, y - 1))
        if in_bounds(x, y + 1):
            vision.add((x, y + 1))
        if in_bounds(x + 1, y - 1):
            vision.add((x + 1, y - 1))
        if in_bounds(x + 1, y):
            vision.add((x + 1, y))
        if in_bounds(x + 1, y + 1):
            vision.add((x + 1, y + 1))
        return vision


    def bishop_vision(self, board, x, y, vision): # Vision is given a list of coordinates: [(x,y), (x2, y2)]
        vision[(x,y)][(1, 1)] = self.get_vision_loop(board, x, y, 1, 1)
        vision[(x,y)][(-1, -1)] = self.get_vision_loop(board, x, y, -1, -1)
        vision[(x,y)][(-1, 1)] = self.get_vision_loop(board, x, y, -1, 1)
        vision[(x,y)][(1, -1)] = self.get_vision_loop(board, x, y, 1, -1)


    def rook_vision(self, board, x, y, vision): # Vision is given a list of coordinates: [(x,y), (x2, y2)]
        vision[(x,y)][(1, 0)] = self.get_vision_loop(board, x, y, 1, 0)
        vision[(x,y)][(-1, 0)] = self.get_vision_loop(board, x, y, -1, 0)
        vision[(x,y)][(0, 1)] = self.get_vision_loop(board, x, y, 0, 1)
        vision[(x,y)][(0, -1)] = self.get_vision_loop(board, x, y, 0, -1)
    

    def knight_vision(self, x, y):
        vision = set()
        if in_bounds(x - 2, y - 1):
            vision.add((x - 2, y - 1))
        if in_bounds(x - 2, y + 1):
            vision.add((x - 2, y + 1))
        if in_bounds(x + 2, y - 1):
            vision.add((x + 2, y - 1))
        if in_bounds(x + 2, y + 1):
            vision.add((x + 2, y + 1))
        if in_bounds(x - 1, y - 2):
            vision.add((x - 1, y - 2))
        if in_bounds(x - 1, y + 2):
            vision.add((x - 1, y + 2))
        if in_bounds(x + 1, y - 2):
            vision.add((x + 1, y - 2))
        if in_bounds(x + 1, y + 2):
            vision.add((x + 1, y + 2))
        return vision

    # Dictionary mapping pieces to Vision.
    # For pawns, kings, and knights, Vision is just a list of positions that are in the piece's line-of-sight.
    # For rooks, bishops, and queens, Vision is a map: { direction: list of positions in the piece's line-of-sight }.
    #   - Here, direction refers to one of the 8 directions (-1, 0), (1, 1), ...  
    def recalc_vision(self, board):
        vision = {}
        for x, y in sorted(self.pieces):
            p = board[x][y]
            typ = p.lower()
            if typ == 'p':
                vision[(x,y)] = set()
                if in_bounds(x + 1, y + self.forwards_movement):
                    vision[(x,y)].add((x + 1, y + self.forwards_movement))
                if in_bounds(x - 1, y + self.forwards_movement):
                    vision[(x,y)].add((x - 1, y + self.forwards_movement))
            elif typ == 'k':
                vision[(x,y)] = self.king_vision(x, y)
            elif typ == 'n':
                vision[(x,y)] = self.knight_vision(x, y)
            else:
                vision[(x,y)] = {}
                if typ == 'r' or typ == 'q':
                    self.rook_vision(board, x, y, vision)
                if typ == 'b' or typ == 'q':
                    self.bishop_vision(board, x, y, vision)
        
        return vision
    
    def recompute_all_attacking_locs(self, vision):
        all_attacking_locs = set()
        for loc in vision:
            if type(vision[loc]) == dict:
                for key in vision[loc]:
                    all_attacking_locs |= vision[loc][key]
            else:
                all_attacking_locs |= vision[loc]
        return all_attacking_locs
    
    # NOTE: Doesn't check en pessant attacks!
    def check_can_castle(self, board, loc):
        # Check if knight is attacking
        knight_piece = make_piece(self.color, 'n')
        for knight_loc in self.knight_vision(loc[0], loc[1]):
            if board[knight_loc[0]][knight_loc[1]] == knight_piece:
                return True

        # Check if pawn is attacking
        pawn_piece = make_piece(self.color, 'p')
        if in_bounds(loc[0] + 1, loc[1] - self.forwards_movement):
            if board[loc[0] + 1][loc[1] - self.forwards_movement] == pawn_piece:
                return True
        if in_bounds(loc[0] - 1, loc[1] - self.forwards_movement):
            if board[loc[0] - 1][loc[1] - self.forwards_movement] == pawn_piece:
                return True
        
        # Check if king is attacking
        king_piece = make_piece(self.color, 'k')
        for king_loc in self.king_vision(loc[0], loc[1]):
            if board[king_loc[0]][king_loc[1]] == king_piece:
                return True
        
        # Check if rook / bishop / queen are attacking
        rook_piece = make_piece(self.color, 'r')
        bishop_piece = make_piece(self.color, 'b')
        queen_piece = make_piece(self.color, 'q')
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            attacking_pieces = rook_piece + queen_piece if dx == 0 or dy == 0 else bishop_piece + queen_piece
            for d in range(1, 9):
                if not in_bounds(loc[0] + d*dx, loc[1] + d*dy):
                    break
                board_piece = board[loc[0] + d*dx][loc[1] + d*dy]
                if board_piece != 'e':
                    if board_piece in attacking_pieces:
                        return True
                    break
