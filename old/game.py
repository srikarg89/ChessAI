from helpers import *
from threading import Thread

class Game:
    def __init__(self, display_type):
        self.display = display_type(self)
        self.board = get_starting_board()
        self.display.set_board(self.board)
        self.display.render()
        self.over = False
        self.turn = True # True = white's turn, False = black's turn
        self.piece_moved = [[False for i in range(8)] for j in range(8)]
        self.moves = []


    def run(self):
        while not self.over:
            self.display.check_action()
            self.display.render()
    

    def check_wall(self, x, y):
        return x < 0 or y < 0 or x >= 8 or y >= 8


    def check_ally_present(self, x, y, piece):
        if self.check_wall(x, y):
            return False
        target = get_pos(self.board, x, y)
        return (is_white(piece) and is_white(target)) or (is_black(piece) and is_black(target))


    def check_enemy_present(self, x, y, piece):
        if self.check_wall(x, y):
            return False
        target = get_pos(self.board, x, y)
        return (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target))


    def get_possible_moves_loop(self, piece, x, y, dx, dy, poss):
        for d in range(1, 9):
            if self.check_wall(x + d*dx, y + d*dy) or self.check_ally_present(x + d*dx, y + d*dy, piece):
                break
            poss.append(Move((x,y), (x + d*dx, y + d*dy), piece))
            if self.check_enemy_present(x + d*dx, y + d*dy, piece):
                break


    def get_possible_moves(self, x, y, piece):
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
                    if self.check_wall(x + dx, y + dy) or self.check_ally_present(x + dx, y + dy, piece):
                        continue
                    poss.append(Move((x,y), (x + dx, y + dy), piece))
                    # TODO: Check if you're walking into a check

            # Castling
            king_moved = self.piece_moved[4][backrank]
            rooks_moved = (self.piece_moved[0][backrank], self.piece_moved[7][backrank])
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
                    if self.check_wall(x + dx, y + dy) or self.check_ally_present(x + dx, y + dy, piece):
                        continue
                    poss.append(Move((x,y), (x + dx, y + dy), piece))

        # Pawn moves
        if piece.lower() == 'p':
            # Forward moves
            if not self.check_wall(x, y + direction) and get_pos(self.board, x, y + direction * 1) == 'e':
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

        # TODO: Add promotion
        # TODO: If a move leaves you in check, you can't do it
        # TODO: Add game termination (draws, stalemate, checkmate)
        return poss
    
    def in_check(self, color):
        pass

    
    def make_move(self, move: Move):
        piece = move.piece
        x, y = move.prev_pos
        targetX, targetY = move.new_pos
        if is_white(piece) and not self.turn:
            return
        if is_black(piece) and self.turn:
            return
        poss = self.get_possible_moves(x, y, piece)
        move = move_in_arr(move, poss) # Check if the move is possible + if it's a special move
        if move: # If you can make the move, make it
            specialty = move.specialty
            print("Making move: ", move)
            place(self.board, targetX, targetY, piece)
            backrank = 0 if is_white(piece) else 7
            # Castling, move rooks to proper spot
            if specialty == 'O-O':
                place(self.board, 7, backrank, 'e')
                place(self.board, 5, backrank, 'R' if is_white(piece) else 'r')
                self.piece_moved[7][backrank] = True
            elif specialty == 'O-O-O':
                place(self.board, 0, backrank, 'e')
                place(self.board, 3, backrank, 'R' if is_white(piece) else 'r')
                self.piece_moved[0][backrank] = True
            elif specialty == 'EP': # Pawn at new x and old y is captured
                place(self.board, move.new_pos[0], move.prev_pos[1], 'e')
                self.piece_moved[move.new_pos[0]][move.prev_pos[1]] = True

            self.turn = not self.turn
            self.moves.append(move)
            self.piece_moved[move.prev_pos[0]][move.prev_pos[1]] = True
            self.piece_moved[move.new_pos[0]][move.new_pos[1]] = True
        else:
            place(self.board, x, y, piece) # Move the piece back



