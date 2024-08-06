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

            # Dictionary mapping pieces to Vision.
            # For pawns, kings, and knights, Vision is just a list of positions that are in the piece's line-of-sight.
            # For rooks, bishops, and queens, Vision is a map: { direction: list of positions in the piece's line-of-sight }.
            #   - Here, direction refers to one of the 8 directions (-1, 0), (1, 1), ...  
            self.vision = self.recalc_vision(board)
            self.all_attacking_locs = self.recompute_all_attacking_locs()

    def make_copy(self, board) -> "Player":
        new_player = Player(self.color, board, run_constructor=False)

        new_player.king_has_moved = self.king_has_moved
        new_player.lrook_has_moved = self.lrook_has_moved
        new_player.rrook_has_moved = self.rrook_has_moved

        new_player.pieces = self.pieces.copy()
        new_player.king_pos = self.king_pos

        new_player.vision = {}
        for loc in self.vision:
            if type(self.vision[loc]) == dict:
                new_item = {}
                for key in self.vision[loc]:
                    new_item[key] = self.vision[loc][key].copy()
            else:
                new_item = self.vision[loc].copy()
            new_player.vision[loc] = new_item
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
        for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            if in_bounds(x + dx, y + dy):
                vision.add((x + dx, y + dy))
        return vision

    def update_vision_single(self, piece, x, y, board, move: Move):
        typ = piece.lower()
        # King vision only gets updated when it moves.
        if typ == 'k':
            if move.new_pos == (x,y):
                self.vision[(x,y)] = self.king_vision(x,y)

        # Knight vision only gets updated when it moves.
        elif typ == 'n':
            if move.new_pos == (x,y):
                self.vision[(x,y)] = self.knight_vision(x,y)
        
        # Pawn vision is fast enough to recalculate manually each time.
        elif typ == 'p':
            self.vision[(x,y)] = set()
            if in_bounds(x + 1, y + self.forwards_movement):
                self.vision[(x,y)].add((x + 1, y + self.forwards_movement))
            if in_bounds(x - 1, y + self.forwards_movement):
                self.vision[(x,y)].add((x - 1, y + self.forwards_movement))

        # Bishops, rooks, and queens, want to recalculate vision if the piece itself moved,
        # They also want to recalculate vision if a piece moved into or out of its vision,
        # but only recalculate on that one branch.
        elif typ in {*'rbq'}:
            if move.new_pos == (x,y):
                self.vision[(x,y)] = {}
                if typ == 'r':
                    self.rook_vision(board, x, y, self.vision)
                elif typ == 'b':
                    self.bishop_vision(board, x, y, self.vision)
                elif typ == 'q':
                    self.rook_vision(board, x, y, self.vision)
                    self.bishop_vision(board, x, y, self.vision)
            else:
                # Check if any of the vision branches need to be updated.
                capture_pos = get_captured_pos(board, move)
                pos_to_worry_about = {move.prev_pos, move.new_pos, capture_pos}
                pos_diffs = [(pos[0] - x, pos[1] - y) for pos in pos_to_worry_about]
                for pos_diff in pos_diffs:
                    if typ in 'rq':
                        # In the same row as the piece.
                        if pos_diff[1] == 0:
                            dx, dy = (1, 0) if pos_diff[0] > 0 else (-1, 0)
                            self.vision[(x,y)][(dx,dy)] = self.get_vision_loop(board, x, y, dx, dy)

                        # In the same col as the piece.
                        elif pos_diff[0] == 0:
                            dx, dy = (0, 1) if pos_diff[1] > 0 else (0, -1)
                            self.vision[(x,y)][(dx,dy)] = self.get_vision_loop(board, x, y, dx, dy)

                    if typ in 'bq':
                        # In the same positive diagonal as the piece.
                        if pos_diff[0] == pos_diff[1]:
                            dx, dy = (1, 1) if pos_diff[0] > 0 else (-1, -1)
                            self.vision[(x,y)][(dx,dy)] = self.get_vision_loop(board, x, y, dx, dy)

                        # In the same negative diagonal as the piece.
                        elif pos_diff[0] == -pos_diff[1]:
                            dx, dy = (1, -1) if pos_diff[0] > 0 else (-1, 1)
                            self.vision[(x,y)][(dx,dy)] = self.get_vision_loop(board, x, y, dx, dy)


    def update_vision(self, board, last_move):
        # If you just moved from somewhere, remove that location from the vision.
        if last_move.prev_pos in self.vision:
            del self.vision[last_move.prev_pos]
        
        # If your piece just got captured, remove that location from the vision.
        capture_loc = get_captured_pos(board.board, last_move)
        if capture_loc is not None and capture_loc in self.vision and capture_loc not in self.pieces:
            del self.vision[capture_loc]

        for x, y in self.pieces:
            p = board.board[x][y]
            self.update_vision_single(p, x, y, board.board, last_move)
            
        self.all_attacking_locs = self.recompute_all_attacking_locs()


    def recalc_vision(self, board):
        vision = {}
        for x, y in self.pieces:
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
    
    def recompute_all_attacking_locs(self):
        all_attacking_locs = set()
        for loc in self.vision:
            if type(self.vision[loc]) == dict:
                for key in self.vision[loc]:
                    all_attacking_locs |= self.vision[loc][key]
            else:
                all_attacking_locs |= self.vision[loc]
        return all_attacking_locs
