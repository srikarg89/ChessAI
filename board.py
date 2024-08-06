from base import *
from player import Player

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

class Board:
    def __init__(self, call_constructor=True):
        if call_constructor:
            self.board = get_starting_board()
            self.turn = Color.WHITE
            self.moves = []
            self.white = Player(Color.WHITE, self.board)
            self.black = Player(Color.BLACK, self.board)
            self.players = {
                Color.WHITE: self.white,
                Color.BLACK: self.black
            }

    def make_copy(self):
        new_board = Board(False)
        new_board.board = [row.copy() for row in self.board]
        new_board.moves = [move.copy() for move in self.moves]
        new_board.turn = self.turn

        new_board.white = self.white.make_copy(new_board.board)
        new_board.black = self.black.make_copy(new_board.board)
        new_board.players = {
            Color.WHITE: new_board.white,
            Color.BLACK: new_board.black
        }
        return new_board

    def check_enemy_present(self, x, y, piece):
        if not in_bounds(x, y) or piece == 'e':
            return False
        if is_white(piece):
            return is_black(self.board[x][y])
        else:
            return is_white(self.board[x][y])

    # Check if castling is valid, and return a list of possible castling moves
    def get_castling_moves(self, color):
        # Can't castle if the king has moved.
        player = self.players[color]
        if player.king_has_moved:
            return []

        backrank = player.startrank
        opp_attacking_locs = self.players[color.opp()].all_attacking_locs

        # Can't castle out of check
        if (4, backrank) in opp_attacking_locs:
            return []

        poss = []
        
        # Check if we can castle on the short (right) side.
        if not player.rrook_has_moved:
            if (5, backrank) not in opp_attacking_locs and (6, backrank) not in opp_attacking_locs:
                poss.append(Move((4, backrank), (6, backrank), make_piece(color, 'k'), specialty='O-O'))

        # Check if we can castle on the long (left) side.
        if not player.lrook_has_moved:
            if (1, backrank) not in opp_attacking_locs and (2, backrank) not in opp_attacking_locs and (3, backrank) not in opp_attacking_locs:
                poss.append(Move((4, backrank), (2, backrank), make_piece(color, 'k'), specialty='O-O-O'))

        return poss

    # TODO: Move differential instead of recalculating every move
    def get_possible_moves(self, allow_king_capturing=False):
        player = self.players[self.turn]
        opp_player = self.players[self.turn.opp()]
        # Things not included in vision: Pawn moving forward (also double forward on first move, and potential promotion), castling, en pessant.
        # Also have to check if a certain move leads to getting checked
            # 1) You could already be in check, and ur move doesn't help u get out of it
            # 2) You're a random piece and were blocking a check and you moved out of the way
            # 3) You're the king and you moved into check
            # Easiest way to do this is to just apply the move and then check if ur king is in the opponent's vision
        poss = []
        for x,y in player.vision:
            piece = self.board[x][y]
            if piece.lower() == 'p':
                # Forwards movement for pawns
                infront = (x, y + player.forwards_movement)
                # Check that the square in front of you is not blocked
                if in_bounds(infront[0], infront[1]) and self.board[infront[0]][infront[1]] == 'e':
                    # Check if you can promote being moving forwards one square
                    if y + player.forwards_movement == player.endrank:
                        poss.append(Move((x, y), infront, piece, specialty='pQ'))
                        poss.append(Move((x, y), infront, piece, specialty='pR'))
                        poss.append(Move((x, y), infront, piece, specialty='pB'))
                        poss.append(Move((x, y), infront, piece, specialty='pN'))
                    # If not, its just a normal pawn move to move forwards
                    else:
                        poss.append(Move((x,y), infront, piece))
                    # Check if you can double move
                    double_infront = (x, y + player.forwards_movement*2)
                    if y == player.startrank + player.forwards_movement and self.board[double_infront[0]][double_infront[1]] == 'e':
                        poss.append(Move((x,y), double_infront, piece))
                
                # Sideways movements (capturing)
                for x2,y2 in player.vision[(x,y)]:
                    # En pessant
                    if len(self.moves) > 0 and self.moves[-1].piece.lower() == 'p' and self.moves[-1].prev_pos == (x2, opp_player.endrank + opp_player.forwards_movement) and self.moves[-1].new_pos == (x2, y):
                        poss.append(Move((x,y), (x2, y2), piece, specialty='EP'))
                    # Regular capture
                    elif self.check_enemy_present(x2, y2, piece):
                        poss.append(Move((x,y), (x2, y2), piece))

            # Knights and kings can move to anywhere in their vision.
            elif piece.lower() == 'k' or piece.lower() == 'n':
                for tX, tY in player.vision[(x,y)]:
                    poss.append(Move((x,y), (tX, tY), piece))

            else:
                # Bishops, rooks, and queens can move to anywhere in their vision, but the vision is a dict of sets not just a set.
                for dir_vision in player.vision[(x,y)].values():
                    for tX, tY in dir_vision:
                        poss.append(Move((x,y), (tX, tY), piece))

        # Add in castling moves
        for move in self.get_castling_moves(self.turn):
            poss.append(move)

        # Filter out capturing ur own piece
        poss = [move for move in poss if move.new_pos not in player.pieces]

        # If allow_king_capturing is enabled, exit early instead of checking if the move leads to a check.
        if allow_king_capturing:
            return poss

        # Apply each move and see if it leads to check. If not, its a valid move!
        valid = []
        for move in poss:
            new_board = self.apply_move(move)
            if new_board.players[self.turn].king_pos not in new_board.players[new_board.turn].all_attacking_locs:
                valid.append(move)

        return valid

    def get_captured_piece(self, move: Move):
        capture_pos = get_captured_pos(self.board, move)
        return None if capture_pos is None else self.board[capture_pos[0]][capture_pos[1]]

    # ASSUMES THAT THE MOVE IS VALID !!!
    def apply_move(self, move: Move):
        piece, specialty = move.piece, move.specialty
        x, y = move.prev_pos
        targetX, targetY = move.new_pos
        new_board = self.make_copy()

        # Check for capture.
        captured_piece = self.get_captured_piece(move)
        if captured_piece is not None:
            if move.specialty is None:
                captured_loc = (targetX, targetY)
            else:
                captured_loc = (targetX, y)
            new_board.players[self.turn.opp()].remove_piece(captured_loc)

        # Move piece
        new_board.board[x][y] = 'e'
        new_board.board[targetX][targetY] = piece
        new_board.players[self.turn].move_piece((x, y), (targetX, targetY))

        if self.board[x][y].lower() == 'k':
            new_board.players[self.turn].king_pos = (targetX, targetY)

        # Add any special functionality
        backrank = new_board.players[self.turn].startrank
        if specialty is not None:
            # En pessant
            if specialty == 'EP':
                new_board.board[targetX][y] = 'e'
            # Short castle
            elif specialty == 'O-O':
                new_board.board[7][backrank] = 'e'
                new_board.board[5][backrank] = make_piece(self.turn, 'r')
                new_board.players[self.turn].move_piece((7, backrank), (5, backrank))
            # Long castle
            elif specialty == 'O-O-O':
                new_board.board[0][backrank] = 'e'
                new_board.board[3][backrank] = make_piece(self.turn, 'r')
                new_board.players[self.turn].move_piece((0, backrank), (3, backrank))
            # Pawn promotion
            elif specialty[0] == 'p':
                new_board.board[targetX][targetY] = make_piece(self.turn, specialty[1])
                new_board.players[self.turn].remove_piece((x, y))
                new_board.players[self.turn].add_piece((targetX, targetY), specialty[1])

        # Update new_board variables that would have changed
        if piece.lower() == 'k':
            new_board.players[self.turn].king_has_moved = True
        if (x,y) == (0, backrank):
            new_board.players[self.turn].lrook_has_moved = True
        if (x,y) == (7, backrank):
            new_board.players[self.turn].rrook_has_moved = True

        new_board.turn = self.turn.opp()
        new_board.moves.append(move)
        new_board.players[Color.WHITE].update_vision(new_board.board, move)
        new_board.players[Color.BLACK].update_vision(new_board.board, move)

        return new_board

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
