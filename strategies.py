import chess
import random
import numpy as np
from chess.engine import PlayResult
from typing import Any


class RandomMove:
    """Get a random move."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)

class Pyrarucu:
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """TODO"""
        return None