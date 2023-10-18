"""
Some example strategies for people who want to create a custom, homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult
import random
from engine_wrapper import MinimalEngine
from typing import Any, Union
import logging
INFINITY = 1e9
MOVE = Union[chess.engine.PlayResult, list[chess.Move]]


# Use this logger variable to print messages to the console or log files.
# logger.info("message") will always print "message" to the console or log file.
# logger.debug("message") will only print "message" if verbose logging is enabled.
logger = logging.getLogger(__name__)

engine_name = 'MyBot'

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
        move, evaluation = self.alpha_beta_pruning(board, 3, -INFINITY, INFINITY, chess.Move.null())
        return PlayResult(move, None)

    def simple_evaluation(self, board: chess.Board) -> float:
        # Heuristics against checkmate
        if board.is_checkmate():
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

        number_legal_moves = len(list(board.legal_moves))
        evaluation = number_legal_moves * .1 + sum_pieces_values
        return evaluation

    def alpha_beta_pruning(self, board: chess.Board, depth: int, alpha: double, beta: double, last_move: chess.Move) -> Tuple[chess.Move, int]:
        if depth == 0 or board.is_checkmate():
            return last_move, self.simple_evaluation(board)

        all_moves = list(board.generate_legal_moves())
        value = -INFINITY if board.turn else INFINITY
        best_move = last_move

        if board.turn:
            for move in all_moves:
                board.push(move)
                child_move, child_evaluation = self.alpha_beta_pruning(board, depth - 1, alpha, beta, move)
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
                child_move, child_evaluation = self.alpha_beta_pruning(board, depth - 1, alpha, beta, move)
                board.pop()

                if child_evaluation < value:
                    best_move = move
                    value = child_evaluation

                # Alpha cutoff
                if value < alpha:
                    break

                beta = min(value, beta)

        return best_move, value

# Example of Simple Bot
# Inherit ExampleEngine and implement search() function
class RandomMove(ExampleEngine):
    """Get a random move."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    """Get the first move when sorted by san representation."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose the first move alphabetically."""
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Get the first move when sorted by uci representation."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose the first move alphabetically in uci representation."""
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)


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
