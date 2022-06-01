from helpers import *
from board import Board
import time

class AI:

    def __init__(self):
        self.cache = {}


    def calc_score(self, board):
        # white_pieces = board.get_all_pieces(Color.WHITE)
        # black_pieces = board.get_all_pieces(Color.BLACK)
        return board.white_heuristic - board.black_heuristic
        # return self.heuristic(board.board, white_pieces) - self.heuristic(board.board, black_pieces)
        # return 1


    def minimax(self, board, color, depth):
        self.counts += 1
        poss = board.get_possible_moves()
        scores = {}
        for move in poss:
            new_board = board.apply_move(move)
            if depth <= 1: # Depth = 1 => Return best move
                scores[move] = self.calc_score(new_board)
            else: # Otherwise, run minimax at one depth lower
                _, best_score = self.minimax(new_board, opp_color(color), depth - 1)
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
            move_score = self.calc_score(new_board) if depth <= 1 else self.alphabeta(new_board, opp_color(color), depth - 1, best_score)[1]
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
        ret, temp = self.minimax(board, board.turn, 3)
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
