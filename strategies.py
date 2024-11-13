import random
from typing import Any

import chess
import numpy as np
from chess.engine import PlayResult


class RandomMove:
    """Get a random move."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)

class Pyrarucu:

    def __init__(self) -> None:
        self.piece_values  = {
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9,
            'K': 1,
            'p': -1,
            'n': -3,
            'b': -3,
            'r': -5,
            'q': -9,
            'k': -1,
        }

    def evaluate(self, board: chess.Board, *args: Any) -> float:
        val = 0


        if board.is_game_over():
            if board.is_checkmate():
                if board.outcome().winner == True:
                    return float('inf')
                else:
                    return -float('inf')
            else:
                return 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                val += self.piece_values[chess.Piece.symbol(piece)]

        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]

        for square in center_squares:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    val += 20
                else:
                    val -= 20
        
        return val
   

    def search(self, board: chess.Board, depth:int=0, alpha:float = -float('inf'), beta:float=float('inf'), *args: Any):
        if depth > 4:
            return None, self.evaluate(board)

        else:
            best_move = None
            best_val = 0
            if board.turn == chess.WHITE:
                best_val = -float('inf')
                best_move = None
                
                for move in board.legal_moves:
                    board.push(move)
                    _, move_val = self.search(board, depth + 1, alpha, beta)
                    board.pop()


                    if(move_val > best_val):
                        best_move = move
                        best_val = move_val

                    alpha = max(alpha, best_val)
                    if beta <= alpha:
                        break
                            
            else:
                best_val = float('inf')
                best_move = None
                
                for move in board.legal_moves:
                    board.push(move)
                    _, move_val = self.search(board, depth + 1, alpha, beta)
                    board.pop()

                    if(move_val < best_val):
                        best_move = move
                        best_val = move_val

                    beta = min(beta, best_val)
                    if beta <= alpha:
                        break

                
        return best_move, best_val


