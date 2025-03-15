import chess
import chess.engine

from strategies import Pyrarucu, RandomMove
from board import *

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    gui = ChessGUI(screen)
    pygame.quit()

if __name__ == "__main__":
    print("Iniciando jogo de xadrez")
    main()
        
