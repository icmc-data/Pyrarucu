from __future__ import annotations
import chess
from chess.engine import PlayResult
import random
from engine_wrapper import MinimalEngine
from typing import Any, Union
import logging
import pickle
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import HistGradientBoostingRegressor


INFINITY = 1e9
SEARCH_DEPTH = 3
engine_name = 'MyBot'
MOVE = Union[chess.engine.PlayResult, list[chess.Move]]
logger = logging.getLogger(__name__)

model_filename = 'engines/model.pkl'

model = pickle.load(open(model_filename, 'rb'))

class BitboardHelper:
    @staticmethod
    def bitboards_to_array(bb: np.ndarray) -> np.ndarray:
        bb = np.asarray(bb, dtype=np.uint64)[:, np.newaxis]
        s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
        b = (bb >> s).astype(np.uint8)
        b = np.unpackbits(b, bitorder="little")
        return list(b)
    
    @staticmethod
    def fen_to_bit_array(fen):
        board = chess.Board(fen=fen)

        black, white = board.occupied_co

        bitboards = np.array([
            black & board.pawns,
            black & board.knights,
            black & board.bishops,
            black & board.rooks,
            black & board.queens,
            black & board.kings,
            white & board.pawns,
            white & board.knights,
            white & board.bishops,
            white & board.rooks,
            white & board.queens,
            white & board.kings,
            board.turn,
            board.has_castling_rights(white),
            board.has_castling_rights(black)
        ], dtype=np.uint64)

        return BitboardHelper.bitboards_to_array(bitboards)


class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""
    pass


class MyBot(ExampleEngine):
    # rnbqkp RNBQKP
    piece_values = {
        'R': 50, 'N': 30, 'B': 30, 'Q': 100, 'K': 1000, 'P': 10, # White
        'r': -50, 'n': -30, 'b': -30, 'q': -100, 'k': -1000, 'p': -10 # Black
    }

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        move, evaluation = self.alpha_beta_pruning(board, SEARCH_DEPTH, -INFINITY, INFINITY, chess.Move.null())
        return PlayResult(move, None)

    def eval_move(self, board, move):
        board.push(move)
        evaluation = self.simple_evaluation(board)
        board.push(chess.Move.null())
        board.pop()
        board.pop()

        print(move, evaluation)
        return evaluation

    def simple_evaluation(self, board: chess.Board) -> float:
        # Heuristics against checkmate
        if board.is_checkmate() or board.is_check():
            if board.turn == chess.WHITE:
                return -1000
            else:
                return 1000

        # Simple Evaluation Function
        sum_pieces_values = 0
        board_fen: str = board.board_fen()
        for char in board_fen:
            try:
                char_value = self.piece_values[char]
            except KeyError:
                char_value = 0
            sum_pieces_values += char_value

        number_legal_moves = board.legal_moves.count()
        evaluation = number_legal_moves * 0.5 + sum_pieces_values
        return evaluation

    def ml_evaluation(self, board: chess.Board) -> float:
        bitboard = BitboardHelper.fen_to_bit_array(board.board_fen())
        evaluation = model.predict([bitboard])[0]
        return evaluation

    def alpha_beta_pruning(
        self, board: chess.Board, 
        depth: int, alpha: double, 
        beta: double, last_move: chess.Move) -> Tuple[chess.Move, int]:
        
        if depth <= 0 or board.is_checkmate():
            return last_move, self.ml_evaluation(board)

        all_moves = list(board.generate_legal_moves())
        value = -INFINITY if board.turn else INFINITY

        # Sort moves when max depth
        if depth == SEARCH_DEPTH:
            all_moves = sorted(all_moves, key=lambda move: self.eval_move(board, move), reverse=board.turn)

        best_move = last_move
        
        # Get only top moves
        n_moves_to_analyze = int((depth / SEARCH_DEPTH) * len(all_moves)) + 1
        best_moves = all_moves[:n_moves_to_analyze]

        depth = depth - 1
        if board.turn:
            for i in range(len(best_moves)):                    
                move = best_moves[i]
                board.push(move)
                child_move, child_evaluation = self.alpha_beta_pruning(board, depth, alpha, beta, move)
                board.pop()
                
                if child_evaluation > value:
                    best_move = move
                    value = child_evaluation

                # Beta cutoff
                if value > beta:
                    break

                alpha = max(value, alpha)
        else:
            for move in all_moves:
                board.push(move)
                child_move, child_evaluation = self.alpha_beta_pruning(board, depth, alpha, beta, move)
                board.pop()

                if child_evaluation < value:
                    best_move = move
                    value = child_evaluation

                # Alpha cutoff
                if value < alpha:
                    break

                beta = min(value, beta)

        return best_move, value


## -------------------------------------------------------------------------- ##
## -------------------- EXAMPLES ---------------------------------------------##

# Example of Simple Bot
# Inherit ExampleEngine and implement search() function
class RandomMove(ExampleEngine):
    """Get a random move."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)


class ComboEngine(ExampleEngine):
    """
    Get a move using multiple different methods.

    This engine demonstrates how one can use `time_limit`, `draw_offered`, and `root_moves`.
    """

    def search(self, board: chess.Board, time_limit: chess.engine.Limit, ponder: bool, draw_offered: bool,
               root_moves: MOVE) -> chess.engine.PlayResult:
        """
        Choose a move using multiple different methods.

        :param board: The current position.
        :param time_limit: Conditions for how long the engine can search (e.g. we have 10 seconds and search up to depth 10).
        :param ponder: Whether the engine can ponder after playing a move.
        :param draw_offered: Whether the bot was offered a draw.
        :param root_moves: If it is a list, the engine should only play a move that is in `root_moves`.
        :return: The move to play.
        """
        if isinstance(time_limit.time, int):
            my_time = time_limit.time
            my_inc = 0
        elif board.turn == chess.WHITE:
            my_time = time_limit.white_clock if isinstance(time_limit.white_clock, int) else 0
            my_inc = time_limit.white_inc if isinstance(time_limit.white_inc, int) else 0
        else:
            my_time = time_limit.black_clock if isinstance(time_limit.black_clock, int) else 0
            my_inc = time_limit.black_inc if isinstance(time_limit.black_inc, int) else 0

        possible_moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)

        if my_time / 60 + my_inc > 10:
            # Choose a random move.
            move = random.choice(possible_moves)
        else:
            # Choose the first move alphabetically in uci representation.
            possible_moves.sort(key=str)
            move = possible_moves[0]
        return PlayResult(move, None, draw_offered=draw_offered)
