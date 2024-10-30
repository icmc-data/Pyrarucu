import chess
import chess.engine
from strategies import RandomMove
from gui import ChessGUI

def print_styled(board: chess.Board) -> None:
    print("Black")
    print(board.unicode(invert_color=True))
    print("White")
    print()


def play_against_engine(engine: chess.engine):
    board = chess.Board()
    print("Let's play a game of Chess. I take the white pieces!")
    print_styled(board)

    while not board.is_game_over():
        result = engine.search(board)
        board.push(result.move)
        print_styled(board)

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
        
        print_styled(board)

    print('Game finished!')
    print(board.outcome().result())


def main():
    engine = RandomMove()
    gui = ChessGUI()
    gui.play_engine(engine)

if __name__ == '__main__':
    main()

        
