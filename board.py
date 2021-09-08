from helpers import *
from threading import Thread

class Board:
    def __init__(self):
        self.board = get_starting_board()
        self.turn = Color.WHITE
        self.moves = []

    def make_copy(self):
        new_board = Board()
        new_board.board = [row.copy() for row in self.board]
        new_board.turn = self.turn
        new_board.moves = [move.copy() for move in self.moves]
        return new_board


    def check_ally_present(self, x, y, piece):
        if not in_bounds((x, y)):
            return False
        target = get_pos(self.board, x, y)
        return (is_white(piece) and is_white(target)) or (is_black(piece) and is_black(target))


    def check_enemy_present(self, x, y, piece):
        if not in_bounds((x, y)):
            return False
        target = get_pos(self.board, x, y)
        return (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target))


    def has_moved(self, x, y):
        for move in self.moves:
            if move.prev_pos == (x,y):
                return True
            if move.specialty == 'O-O':
                if (x,y) == (7,4):
                    return True
            if move.specialty == 'O-O-O':
                if (x,y) == (0,4):
                    return True
        return False


    def get_possible_moves_loop(self, piece, x, y, dx, dy, poss):
        for d in range(1, 9):
            if not in_bounds((x + d*dx, y + d*dy)) or self.check_ally_present(x + d*dx, y + d*dy, piece):
                break
            poss.append(Move((x,y), (x + d*dx, y + d*dy), piece))
            if self.check_enemy_present(x + d*dx, y + d*dy, piece):
                break


    def get_piece_possible_moves(self, x, y, piece):
        backrank = 0 if is_white(piece) else 7
        direction = 1 if is_white(piece) else -1
        poss = []
        # Basic king moves
        if piece.lower() == 'k':
            # Loop through king moves
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    # Move one square in any direction
                    if not in_bounds((x + dx, y + dy)) or self.check_ally_present(x + dx, y + dy, piece):
                        continue
                    poss.append(Move((x,y), (x + dx, y + dy), piece))

            # Castling
            king_moved = self.has_moved(4, backrank)
            rooks_moved = (self.has_moved(0, backrank), self.has_moved(7, backrank))
            if not king_moved:
                if not rooks_moved[0]: # Long castle viable
                    poss.append(Move((x,y), (2, backrank), piece, specialty="O-O-O"))
                if not rooks_moved[1]: # Short castle viable
                    poss.append(Move((x,y), (6, backrank), piece, specialty="O-O"))
            # TODO: Can't castle out of or through check

        # Rook / queen moves
        if piece.lower() == 'r' or piece.lower() == 'q':
            # Check horizontal / vertical motion (rook / queen moves)
            self.get_possible_moves_loop(piece, x, y, 1, 0, poss)
            self.get_possible_moves_loop(piece, x, y, -1, 0, poss)
            self.get_possible_moves_loop(piece, x, y, 0, 1, poss)
            self.get_possible_moves_loop(piece, x, y, 0, -1, poss)

        # Bishop / queen moves
        if piece.lower() == 'b' or piece.lower() == 'q':
            # Check diagonals (bishop / queen moves)
            self.get_possible_moves_loop(piece, x, y, 1, 1, poss)
            self.get_possible_moves_loop(piece, x, y, 1, -1, poss)
            self.get_possible_moves_loop(piece, x, y, -1, 1, poss)
            self.get_possible_moves_loop(piece, x, y, -1, -1, poss)

        # Knight moves
        if piece.lower() == 'n':
            # Loop through possible knight moves
            for dx in [-2, -1, 1, 2]:
                for dy in [-2, -1, 1, 2]:
                    if abs(dx) == abs(dy):
                        continue
                    if not in_bounds((x + dx, y + dy)) or self.check_ally_present(x + dx, y + dy, piece):
                        continue
                    poss.append(Move((x,y), (x + dx, y + dy), piece))

        # Pawn moves
        if piece.lower() == 'p':
            # Forward moves
            if in_bounds((x, y + direction)) and get_pos(self.board, x, y + direction * 1) == 'e':
                if y + direction == 7 - backrank: # Promotion
                    poss.append(Move((x, y), (x, y + direction), piece, specialty='promotion_Q'))
                    poss.append(Move((x, y), (x, y + direction), piece, specialty='promotion_R'))
                    poss.append(Move((x, y), (x, y + direction), piece, specialty='promotion_B'))
                    poss.append(Move((x, y), (x, y + direction), piece, specialty='promotion_N'))
                else:
                    poss.append(Move((x, y), (x, y + direction), piece))
                if y == backrank + direction and get_pos(self.board, x, y + direction * 2) == 'e': # Hasn't moved (still on the second rank)
                    poss.append(Move((x, y), (x, y + direction * 2), piece))
            # Diagonal captures
            targets = [(x + dx, y + direction) for dx in [-1, 1]]
            for target in targets:
                if self.check_enemy_present(target[0], target[1], piece):
                    poss.append(Move((x, y), target, piece))
            # En pessant
            if len(self.moves) > 0:
                opp_color = 'p' if piece == 'P' else 'P'
                opp_pawnrank = 6 if is_white(piece) else 1
                last_move = self.moves[-1]
                if last_move.piece == opp_color and last_move.prev_pos[1] == opp_pawnrank and last_move.new_pos[1] == opp_pawnrank + direction * -2: # Just moved their pawn 2 squares
                    if y == opp_pawnrank + direction * -2 and abs(last_move.new_pos[0] - x) == 1: #If ur pawn is in the right spot
                        target = (last_move.new_pos[0], y + direction)
                        poss.append(Move((x,y), target, piece, specialty='EP'))

        # TODO: Add game termination (draws, stalemate, checkmate)
        return poss
    

    def get_all_pieces(self, color):
        pieces = []
        for x in range(8):
            for y in range(8):
                char = get_pos(self.board, x, y)
                if (color == Color.WHITE and is_white(char)) or (color == Color.BLACK and is_black(char)):
                    pieces.append((x,y))
        return pieces

    def find_piece(self, piece):
        locs = []
        for x in range(8):
            for y in range(8):
                char = get_pos(self.board, x, y)
                if char == piece:
                    locs.append((x,y))
        return locs


    def get_all_possible_moves(self, color):
        poss = []
        pieces = self.get_all_pieces(color)
        for x, y in pieces:
            piece_poss = self.get_piece_possible_moves(x, y, get_pos(self.board, x, y))
            # if self.turn == Color.WHITE:
            #     print(x, y, [m.prev_pos for m in piece_poss])
            poss += piece_poss
        return poss


    def get_legit_moves(self, color):
        poss = self.get_all_possible_moves(color)
        legit = []
        for move in poss:
            new_board = self.apply_move(move)
            if new_board.in_check(color):
                continue
            legit.append(move)
        return legit


    def in_check(self, color):
        opp = opp_color(color)
        opp_direction = get_direction(opp_color)
        poss = self.get_all_possible_moves(opp)
        king_pos = self.find_piece(make_piece(color, 'k'))[0]
        for move in poss:
            if move.piece.lower() != 'p' and move.new_pos == king_pos: # Attacked by a piece
                return True
            elif move.piece.lower() == 'p' and abs(king_pos[0] - move.prev_pos[0]) == 1 and move.prev_pos[1] + opp_direction == king_pos[1]: # Attacked by a pawn
                return True
        # Not being attacked, so not in check
        return False

    
    def apply_move(self, move: Move):
        piece = move.piece
        x, y = move.prev_pos
        targetX, targetY = move.new_pos
        new_board = self.make_copy()
        specialty = move.specialty
        # print("Applying move: ", move)
        place(new_board.board, x, y, 'e')
        place(new_board.board, targetX, targetY, piece)
        backrank = 0 if self.turn == Color.WHITE else 7
        # Castling, move rooks to proper spot
        if specialty == 'O-O':
            place(new_board.board, 7, backrank, 'e')
            place(new_board.board, 5, backrank, make_piece(self.turn, 'r'))
        elif specialty == 'O-O-O':
            place(new_board.board, 0, backrank, 'e')
            place(new_board.board, 3, backrank, make_piece(self.turn, 'r'))
        elif specialty == 'EP': # Pawn at new x and old y is captured
            place(new_board.board, move.new_pos[0], move.prev_pos[1], 'e')
        
        # TODO: Add promotion

        new_board.turn = opp_color(self.turn)
        new_board.moves.append(move)
        return new_board


    def make_move(self, move: Move):
        piece = move.piece
        x, y = move.prev_pos
        targetX, targetY = move.new_pos
        place(self.board, x, y, piece)
        if (is_white(piece) and self.turn == Color.BLACK) or (is_black(piece) and self.turn == Color.WHITE): # Only move on your turn
            return self
        poss = self.get_legit_moves(self.turn)
        # print("Poss:", [m.prev_pos for m in poss])
        move = move_in_arr(move, poss) # Check if the move is possible + if it's a special move
        # print("Move", move)
        if not move: # IF you can't make the move, return the current board
            return self
        else: # If you can make the move, make it
            return self.apply_move(move)
