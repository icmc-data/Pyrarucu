import chess
import chess.engine
from strategies import MyBot
from config import load_config
import logging
import engine_wrapper
lichess_bot = __import__('lichess-bot')

logger = logging.getLogger(__name__)

def play_against_engine(engine: chess.engine):
    board = chess.Board()
    print("Let's play a game of Chess. I take the white pieces!")
    print("Black")
    print(board)
    print("White")
    print()

    while not board.is_game_over():
        result = engine.search(board)
        board.push(result.move)
        print(board)

        valid_move = False

        while not valid_move:
            human_move = input('Insert move in UCI format (a2a4): ')
            move = chess.Move.from_uci(human_move)
            list_valid_moves = board.generate_legal_moves()
            if move in list_valid_moves:
                board.push(move)
                valid_move = True
            else:
                print("Not a valid move!")
        
        print(board)

    print('Game finished!')
    print(board.outcome().result())


def main():
    engine = MyBot(commands=None, options={}, stderr=1, draw_or_resign=False, name='MyBot')
    play_against_engine(engine)
    engine.quit()


if __name__ == '__main__':
    main()

        
