from base import *

# Transposes a given 2D matrix
def transpose(matrix):
    t = []
    for i in range(len(matrix[0])): 
        t.append([])
        for j in range(len(matrix)):
            t[-1].append(matrix[j][i])
    return t

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

def make_piece(color, piece):
    return piece.upper() if color == Color.WHITE else piece.lower()

class Board:
    def __init__(self, call_constructor=True):
        if call_constructor:
            self.board = get_starting_board()
            self.turn = Color.WHITE
            self.moves = []
            self.king_has_moved = {Color.WHITE: False, Color.BLACK: False}
            self.lrook_has_moved = {Color.WHITE: False, Color.BLACK: False}
            self.rrook_has_moved = {Color.WHITE: False, Color.BLACK: False}
            self.white_pieces = self.get_all_pieces(Color.WHITE)
            self.black_pieces = self.get_all_pieces(Color.BLACK)


    def make_copy(self):
        new_board = Board(False)
        new_board.board = [row.copy() for row in self.board]
        new_board.moves = [move.copy() for move in self.moves]
        new_board.turn = self.turn

        new_board.king_has_moved = {i: self.king_has_moved[i] for i in ALL_COLORS}
        new_board.lrook_has_moved = {i: self.lrook_has_moved[i] for i in ALL_COLORS}
        new_board.rrook_has_moved = {i: self.rrook_has_moved[i] for i in ALL_COLORS}

        new_board.white_pieces = [i for i in self.white_pieces]
        new_board.black_pieces = [i for i in self.black_pieces]
        return new_board

    def check_enemy_present(self, x, y, piece):
        if not in_bounds((x, y)) or piece == 'e':
            return False
        if is_white(piece):
            return is_black(self.board[x][y])
        else:
            return is_white(self.board[x][y])

    def get_all_pieces(self, color):
        pieces = []
        for x in range(8):
            for y in range(8):
                char = self.board[x][y]
                if (color == Color.WHITE and is_white(char)) or (color == Color.BLACK and is_black(char)):
                    pieces.append((x,y))
        return pieces

    def find_piece(self, piece):
        locs = []
        for x in range(8):
            for y in range(8):
                char = self.board[x][y]
                if char == piece:
                    locs.append((x,y))
        return locs

    def get_vision_loop(self, x, y, dx, dy, vision): # Vision is given a list of coordinates: [(x, y), (x2, y2)]
        for d in range(1, 9):
            if not in_bounds((x + d*dx, y + d*dy)):
                break
            vision.append((x + d*dx, y + d*dy))
            if self.board[x + d*dx][y + d*dy] != 'e' or self.board[x + d*dx][y + d*dy] != 'e':
                break
        return vision

    def king_vision(self, x, y, vision): # Vision is given a list of coordinates: [(x, y), (x2, y2)]
        if in_bounds2(x - 1, y - 1):
            vision.append((x - 1, y - 1))
        if in_bounds2(x - 1, y):
            vision.append((x - 1, y))
        if in_bounds2(x - 1, y + 1):
            vision.append((x - 1, y + 1))
        if in_bounds2(x, y - 1):
            vision.append((x, y - 1))
        if in_bounds2(x, y + 1):
            vision.append((x, y + 1))
        if in_bounds2(x + 1, y - 1):
            vision.append((x + 1, y - 1))
        if in_bounds2(x + 1, y):
            vision.append((x + 1, y))
        if in_bounds2(x + 1, y + 1):
            vision.append((x + 1, y + 1))
        return vision


    def bishop_vision(self, x, y, vision): # Vision is given a list of coordinates: [(x, y), (x2, y2)]
        vision = self.get_vision_loop(x, y, -1, -1, vision)
        vision = self.get_vision_loop(x, y, -1, 1, vision)
        vision = self.get_vision_loop(x, y, 1, -1, vision)
        vision = self.get_vision_loop(x, y, 1, 1, vision)
        return vision


    def rook_vision(self, x, y, vision): # Vision is given a list of coordinates: [(x, y), (x2, y2)]
        vision = self.get_vision_loop(x, y, 1, 0, vision)
        vision = self.get_vision_loop(x, y, -1, 0, vision)
        vision = self.get_vision_loop(x, y, 0, 1, vision)
        vision = self.get_vision_loop(x, y, 0, -1, vision)
        return vision
    

    def knight_vision(self, x, y, vision):
        for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            if in_bounds((x + dx, y + dy)):
                vision.append((x + dx, y + dy))
        return vision
    
    
    def get_vision(self, color):
        if color == Color.WHITE:
            pieces = self.white_pieces
        else:
            pieces = self.black_pieces
        vision = {}
        for x, y in pieces:
            p = self.board[x][y]
            typ = p.lower()
            vision[(x,y)] = []
            if typ == 'p':
                if in_bounds((x + 1, y + MOVEMENT[color])):
                    vision[(x,y)].append((x + 1, y + MOVEMENT[color]))
                if in_bounds((x - 1, y + MOVEMENT[color])):
                    vision[(x,y)].append((x - 1, y + MOVEMENT[color]))
            elif typ == 'k':
                vision[(x,y)] = self.king_vision(x, y, [])
            elif typ == 'r':
                vision[(x,y)] = self.rook_vision(x, y, [])
            elif typ == 'b':
                vision[(x,y)] = self.bishop_vision(x, y, [])
            elif typ == 'q':
                vision[(x,y)] = self.rook_vision(x, y, self.bishop_vision(x, y, []))
            elif typ == 'n':
                vision[(x,y)] = self.knight_vision(x, y, [])
            
        return vision


    # Check if castling is valid, and return a list of possible castling moves
    def get_castling_moves(self, color):
        if self.king_has_moved[color]:
            return []
        if self.rrook_has_moved[color] and self.lrook_has_moved[color]:
            return []        
        backrank = STARTRANK[color]
        long_spots = [(2, backrank), (3, backrank)]
        short_spots = [(5, backrank), (6, backrank)]
        opp_vision = self.get_vision(color.opp())
        opp_vision_set = set()
        for temp in opp_vision:
            opp_vision_set |= set(opp_vision[temp])

        # Can't castle out of check
        if (4, backrank) in opp_vision_set:
            return []

        poss = []
        tests = [(self.rrook_has_moved[color], short_spots, 6, 'O-O'), (self.lrook_has_moved[color], long_spots, 2, 'O-O-O')]
        for rook_moved, mid_spots, destX, name in tests:
            if rook_moved:
                continue
            works = True
            for midX, midY in mid_spots:
                if self.board[midX][midY] != 'e' or (midX, midY) in opp_vision_set:
                    works = False
                    break
            if works:
                poss.append(Move((4, backrank), (destX, backrank), make_piece(color, 'k'), specialty=name))

        return poss

    # TODO: Move differential instead of recalculating every move
    def get_possible_moves(self):
        color = self.turn
        vision = self.get_vision(color)
        # Things not included in vision: Pawn moving forward (also double forward on first move, and potential promotion), castling, en pessant?
        # Basically a shitton of pawn stuff + capturing + castling
        # Also have to check if a certain move leads to getting checked
            # 1) You could already be in check, and ur move doesn't help u get out of it
            # 2) You're a random piece and were blocking a check and you moved out of the way
            # 3) You're the king and you moved into check
            # Easiest way to do this is to just apply the move and then check if ur king is in the opponent's vision
        poss = []
        for x,y in vision:
            piece = self.board[x][y]
            lower = piece.lower()
            if lower == 'p':
                # Forwards movement for pawns
                infront = (x, y + MOVEMENT[color])
                # Check that the square in front of you is not blocked
                if in_bounds(infront) and self.board[infront[0]][infront[1]] == 'e':
                    # Check if you can promote being moving forwards one square
                    if y + MOVEMENT[color] == ENDRANK[color]:
                        poss.append(Move((x, y), infront, piece, specialty='pQ'))
                        poss.append(Move((x, y), infront, piece, specialty='pR'))
                        poss.append(Move((x, y), infront, piece, specialty='pB'))
                        poss.append(Move((x, y), infront, piece, specialty='pN'))
                    # If not, its just a normal pawn move to move forwards
                    else:
                        poss.append(Move((x,y), infront, piece))
                    # Check if you can double move
                    if y == STARTRANK[color] + MOVEMENT[color] and self.board[infront[0]][infront[1] + MOVEMENT[color]] == 'e':
                        poss.append(Move((x,y), (infront[0], infront[1] + MOVEMENT[color]), piece))
                
                # Sideways movements (capturing)
                for x2,y2 in vision[(x,y)]:
                    # En pessant
                    if len(self.moves) > 0 and self.moves[-1].piece == 'p' and self.moves[-1].prev_pos == (x2, ENDRANK[color] - MOVEMENT[color]) and self.moves[-1].new_pos == (x2, y):
                        poss.append(Move((x,y), (x2, y2), piece, specialty='EP'))
                    # Regular capture
                    elif self.check_enemy_present(x2, y2, piece):
                        poss.append(Move((x,y), (x2, y2), piece))

            elif lower == 'k':
                castling_moves = self.get_castling_moves(color)
                for move in castling_moves:
                    poss.append(move)
                for tX, tY in vision[(x,y)]:
                    poss.append(Move((x,y), (tX, tY), piece))

            else:
                for tX, tY in vision[(x,y)]:
                    poss.append(Move((x,y), (tX, tY), piece))
        
        # Filter out capturing ur own piece
        same_check = is_white if color == Color.WHITE else is_black
        poss = [move for move in poss if not same_check(self.board[move.new_pos[0]][move.new_pos[1]])]

        # Apply each move and see if it leads to check. If not, its a valid move!
        valid = []
        for move in poss:
            new_board = self.apply_move(move)
            new_vision = new_board.get_vision(new_board.turn)
            king_pos = new_board.find_piece(make_piece(color, 'k'))[0]
            works = True
            for key in new_vision:
                if king_pos in new_vision[key]:
                    works = False
                    break
            if works:
                valid.append(move)

        return valid


    # ASSUMES THAT THE MOVE IS VALID !!!
    def apply_move(self, move: Move):
        piece, specialty = move.piece, move.specialty
        x, y = move.prev_pos
        targetX, targetY = move.new_pos
        new_board = self.make_copy()

        # Check for capture.
        captured_piece = self.get_capture_piece(move)
        if captured_piece is not None:
            if move.specialty is None:
                captured_loc = (targetX, targetY)
            else:
                captured_loc = (targetX, y)
            if is_white(captured_piece):
                new_board.white_pieces.remove(captured_loc)
            elif is_black(captured_piece):
                new_board.black_pieces.remove(captured_loc)

        # Move piece
        new_board.board[x][y] = 'e'
        new_board.board[targetX][targetY] = piece
        if new_board.turn == Color.WHITE:
            new_board.white_pieces = [(targetX,targetY) if i == (x,y) else i for i in new_board.white_pieces]
        else:
            new_board.black_pieces = [(targetX,targetY) if i == (x,y) else i for i in new_board.black_pieces]

        # Add any special functionality
        backrank = STARTRANK[self.turn]
        if specialty is not None:
            # En pessant
            if specialty == 'EP':
                new_board.board[targetX][y] = 'e'
            # Short castle
            elif specialty == 'O-O':
                new_board.board[7][backrank] = 'e'
                new_board.board[5][backrank] = make_piece(self.turn, 'r')
            # Long castle
            elif specialty == 'O-O-O':
                new_board.board[0][backrank] = 'e'
                new_board.board[3][backrank] = make_piece(self.turn, 'r')
            # Pawn promotion
            elif specialty[0] == 'p':
                new_board.board[targetX][targetY] = make_piece(self.turn, specialty[1])


        # Update new_board variables that would have changed
        if piece.lower() == 'k':
            new_board.king_has_moved[self.turn] = True
        if (x,y) == (0, backrank):
            new_board.lrook_has_moved[self.turn] = True
        if (x,y) == (7, backrank):
            new_board.rrook_has_moved[self.turn] = True

        new_board.turn = self.turn.opp()
        new_board.moves.append(move)

        return new_board


    # ASSUMES THAT THE MOVE IS VALID !!!
    def get_capture_piece(self, move: Move):
        _, specialty = move.piece, move.specialty
        _, y = move.prev_pos
        targetX, targetY = move.new_pos

        # Check for any special functionality
        if specialty is not None:
            # En pessant
            if specialty == 'EP':
                return self.board[targetX][y]

        return None if self.board[targetX][targetY] == 'e' else self.board[targetX][targetY]


    def make_move(self, move: Move):
        print('----------------------------------------------------------------------------------------------------------')
        x, y = move.prev_pos
        self.board[x][y] = move.piece
        if (is_white(move.piece) and self.turn == Color.BLACK) or (is_black(move.piece) and self.turn == Color.WHITE): # Only move on your turn
            return self
        poss = self.get_possible_moves()
        move = move_in_arr(move, poss) # Check if the move is possible + add specialty to move if needed
        if not move: # IF you can't make the move, return the current board, raise an error??
            return self
        else: # If you can make the move, make it
            return self.apply_move(move)

    # Transposes the board to make the printed output easier to read
    def printboard(self):
        print('\n'.join([''.join(row) for row in transpose(self.board)]))
