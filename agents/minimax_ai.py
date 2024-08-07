from base import *
from . import Agent
from board import Board
import time

def heuristic(board, piece_list):
    score = 0
    value_dict = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 10000}
    for loc in piece_list:
        typ = board[loc[0]][loc[1]].lower()
        score += value_dict[typ]
    return score

# Score is defined as the heuristic for white's team.
def calc_score(board):
    return heuristic(board.board, board.white.pieces) - heuristic(board.board, board.black.pieces)


# TODO: Add pawn promotion to this heuristic!
def get_updated_score(score, board, move):
    captured_piece = board.get_captured_piece(move)
    if captured_piece is None:
        return score

    # Check if the king was captured, and update the heuristics accordingly
    captured_type = captured_piece.lower()
    captured_team = board.turn.opp()
    if captured_type == 'k':
        if captured_team == Color.WHITE:
            return float("-inf")
        return float("inf")

    # Check if a regular piece is being captured, and update the heuristics accordingly
    if captured_team == Color.WHITE:
        return score - PIECE_VALUE[captured_type]
    return score + PIECE_VALUE[captured_type]

class MinimaxAI(Agent):

    def __init__(self, depth, save_history=False):
        self.cache = {}
        self.calcdepth = depth
        self.save_history = save_history
        self.chosen_moves = set()
        if self.save_history:
            self.history = []


    def minimax(self, board, color, depth, prev_score):
        self.counts += 1
        if self.save_history:
            self.history[-1].append([row.copy() for row in board.board])

        best_move = None
        best_score = -float("inf") if color == Color.WHITE else float("inf")
        poss = board.get_possible_moves(allow_king_capturing=True)
        for move in poss:
            new_score = get_updated_score(prev_score, board, move)

            if depth <= 0: # Depth = 0 => Return best move
                score = new_score
            else: # Otherwise, run minimax at one depth lower
                new_board = board.apply_move(move)
                _, score = self.minimax(new_board, color.opp(), depth - 1, new_score)

            # White player tryna maximize the score, black player tryna minimize the score
            if color == Color.WHITE:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move, best_score
        

    # Each round you're trying to maximize your score
    def alphabeta(self, board, color, depth, prev_score, prev_round_known_best=None):
        if self.save_history:
            self.history[-1].append([row.copy() for row in board.board])
        board_string = str(board.board)
        if (board_string, color, depth) in self.cache:
            cached_move = self.cache[(board_string, color, depth)][0]
            # Don't repeat moves.
            if depth == self.calcdepth and (board_string, cached_move.prev_pos, cached_move.new_pos) not in self.chosen_moves:
                return self.cache[(board_string, color, depth)]

        self.counts += 1
        poss = board.get_possible_moves(allow_king_capturing=True)
        best_move = None
        best_score = -float("inf") if color == Color.WHITE else float("inf")
        for move in poss:
            # Don't repeat moves.
            if depth == self.calcdepth and (board_string, move.prev_pos, move.new_pos) in self.chosen_moves:
                continue

            new_score = get_updated_score(prev_score, board, move)

            if depth <= 1:
                score = new_score
            else:
                new_board = board.apply_move(move)
                _, score = self.alphabeta(new_board, color.opp(), depth - 1, new_score, best_score)

            # White player tryna maximize the score, black player tryna minimize the score
            if color == Color.WHITE:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

            # Alpha-beta pruning
            if prev_round_known_best is not None:
                if color == Color.WHITE:
                    if score >= prev_round_known_best:
                        self.cache[(board_string, color, depth)] = (best_move, best_score)
                        return best_move, best_score
                else:
                    if score <= prev_round_known_best:
                        self.cache[(board_string, color, depth)] = (best_move, best_score)
                        return best_move, best_score

        self.cache[(board_string, color, depth)] = (best_move, best_score)
        return best_move, best_score


    def get_move(self, board):
        self.counts = 0
        if self.save_history:
            self.history.append([])
        start = time.time()
        # move, score = self.minimax(board, board.turn, self.calcdepth, calc_score(board))
        move, score = self.alphabeta(board, board.turn, self.calcdepth, calc_score(board))
        self.chosen_moves.add((str(board.board), move.prev_pos, move.new_pos))
        print(move, score)
        print("Time taken to move:", time.time() - start)
        print("Counts:", self.counts)
        return move

"""
Time taken to move: 0.6624670028686523
Counts: 421

"""

"""
            A 4                  BLACK TURN
           /  \
        7 B  |  C 4               WHITE TURN
         / \ | / \
        D   E|F   G
        2   7|1   4
"""
