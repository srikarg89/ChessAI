from base import *
from . import Agent
import time

def heuristic(board, piece_list):
    score = 0
    value_dict = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 10000}
    for loc in piece_list:
        typ = board[loc[0]][loc[1]].lower()
        score += value_dict[typ]
    return score


def calc_score(board):
    return heuristic(board.board, board.white_pieces) - heuristic(board.board, board.black_pieces)


# TODO: Add pawn promotion to this heuristic!
def get_updated_score(score, board, move):
    captured_piece = board.get_capture_piece(move)
    if captured_piece is None:
        return score
    # Check if a piece is being captured, and update the heuristics accordingly
    if is_white(captured_piece):
        return score - PIECE_VALUE[captured_piece.lower()]
    elif is_black(captured_piece):
        return score + PIECE_VALUE[captured_piece.lower()]


class MinimaxAI(Agent):

    def __init__(self):
        self.cache = {}


    def minimax(self, board, color, depth, curr_score):
        self.counts += 1
        poss = board.get_possible_moves()
        scores = {}
        for move in poss:
            new_score = get_updated_score(curr_score, board, move)
            new_board = board.apply_move(move)

            if depth <= 1: # Depth = 1 => Return best move
                scores[move] = new_score
            else: # Otherwise, run minimax at one depth lower
                _, best_score = self.minimax(new_board, color.opp(), depth - 1, new_score)
                scores[move] = best_score

        best_move = None
        best_score = -float("inf") if color == Color.WHITE else float("inf")
        for move in scores:
            # print(move, color == Color.WHITE, scores[move], best_move, best_score)
            if color == Color.WHITE and scores[move] > best_score: # The white player is trying to maximize heuristic
                best_score = scores[move]
                best_move = move
            elif color == Color.BLACK and scores[move] < best_score: # The black player is trying to minimize heuristic
                best_score = scores[move]
                best_move = move

        return best_move, best_score
        

    # Each round you're trying to maximize your score
    def alphabeta(self, board, color, depth, prev_round_known_best=None):
        board_string = str(board.board)
        if (board_string, color, depth) in self.cache:
            return self.cache[(board_string, color, depth)]
        self.counts += 1
        poss = board.get_possible_moves()
        scores = {}
        best_move = None
        best_score = -float("inf") if color == Color.WHITE else float("inf")
        for move in poss:
            new_board = board.apply_move(move)
            # TODO: Use the score updating method not the calc_score method.
            move_score = calc_score(new_board) if depth <= 1 else self.alphabeta(new_board, color.opp(), depth - 1, best_score)[1]
            # White player tryna maximize the score, black player tryna minimize the score
            if (color == Color.WHITE and move_score > best_score) or (color == Color.BLACK and move_score < best_score):
                best_score = move_score
                best_move = move

            # Alpha-beta pruning
            if prev_round_known_best is not None:
                if color == Color.WHITE and move_score >= prev_round_known_best:
                    # print("ALPHA BETA")
                    self.cache[(board_string, color, depth)] = (best_move, best_score)
                    return best_move, best_score
                elif color == Color.BLACK and move_score <= prev_round_known_best:
                    # print("ALPHA BETA")
                    self.cache[(board_string, color, depth)] = (best_move, best_score)
                    return best_move, best_score

        self.cache[(board_string, color, depth)] = (best_move, best_score)
        return best_move, best_score


    def get_move(self, board):
        self.counts = 0
        start = time.time()
        ret, temp = self.minimax(board, board.turn, 3, calc_score(board))
        print(ret, temp)
        # ret = self.alphabeta(board, board.turn, 4)[0]
        print("Time taken to move:", time.time() - start)
        print("Counts:", self.counts)
        return ret

"""
Time taken to move: 8.034504652023315
Counts: 1639


"""

"""
            A 4                  BLACK TURN
           /  \
        7 B  |  C 4               WHITE TURN
         / \ | / \
        D   E|F   G
        2   7|1   4
"""
