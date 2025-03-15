# Interface Gráfica do Tabuleiro de Xadrez (GUI)
# Permite escolher entre os seguintes modos: player (brancas) vs bot e bot vs bot

import chess
import chess.engine
import pygame
import time

from strategies import RandomMove, Pyrarucu

# Definições de dimensões, cores e fonte
pygame.init()
pygame.display.set_caption("Chess Board")
width, height = 640, 640
squareSize = width // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
FONT = pygame.font.Font(None, 36)

PLAYER_BOT = 'p-bot'
BOT_BOT = 'bot-bot'

SYMBOLS = ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']

class ChessGUI:
    def __init__(self, screen: pygame.display):
        self.board = chess.Board()
        self.screen = screen
        self.selected_square = None  # Quadrado inicial da peça selecionada

        self.image_dict = {
            symbol: pygame.image.load(f"images/{symbol}.png") for symbol in SYMBOLS
        }

        self.mode_selection_screen()
        mode = None

        while True:
            if mode != None:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 200 <= x <= 440 and 100 <= y <= 150:
                        mode = PLAYER_BOT
                    elif 200 <= x <= 440 and 160 <= y <= 210:
                        mode = BOT_BOT
        if mode == PLAYER_BOT:
            self.playerVSbot()
        elif mode == BOT_BOT:
            self.botVSbot()

    def draw_board(self):
        colors = [WHITE, GRAY]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                # Desenha um retângulo/tabuleiro
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    pygame.Rect(
                        col * squareSize, 
                        row * squareSize, 
                        squareSize, 
                        squareSize
                    )
                )

    def draw_pieces(self, board: chess.Board):
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_image = self.image_dict[piece.symbol()]
                row = 7 - (square // 8)
                col = square % 8
                # Sobrepõe a imagem da peça sobre o tabuleiro
                self.screen.blit(
                    piece_image, 
                    pygame.Rect(
                        col * (squareSize) + 8, 
                        row * (squareSize) + 10, 
                        squareSize, 
                        squareSize
                    )
                )

    def mode_selection_screen(self):
        pygame.draw.rect(self.screen, GRAY, (200, 100, 240, 50))
        pygame.draw.rect(self.screen, GRAY, (200, 160, 240, 50))

        text_botPlayer = FONT.render("Player vs Bot", True, WHITE)
        text_doubleBot = FONT.render("Bot vs Bot", True, WHITE)
        self.screen.blit(text_botPlayer, (237, 110))
        self.screen.blit(text_doubleBot, (255, 170))

        # Atualiza a tela
        pygame.display.flip()
    
    def promotion_event(self):
        pygame.draw.rect(
            screen, 
            (255, 255, 60), 
            pygame.Rect(
                width // 4, 
                height // 4, 
                width // 2, 
                height // 8
            )
        )

        optionsWhite = ['Q', 'R', 'B', 'N']
        optionsBlack = ['q', 'r', 'b', 'n']

        if self.board.turn == chess.WHITE:
            final = optionsWhite
        else:
            final = optionsBlack

        # Insere na tela as peças de promoção corretas
        for i, piece in enumerate(final):
            piece_image = self.image_dict[final[i]]
            screen.blit(
                piece_image, 
                pygame.Rect(
                    (width // 4) + i * (squareSize + 5), 
                    height // 4, 
                    squareSize, 
                    squareSize
                )
            )

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Verificar qual peça foi clicada
                    if height // 4 < y < (height // 4) + squareSize:
                        for i, piece in enumerate(final):
                            if (width // 4) + i * (squareSize + 5) < x < (width // 4) + (i + 1) * (squareSize + 5):
                                return piece


    # Define o controle das ações e movimentos ao clicar com o mouse
    def handle_mouse_click(self, pos):
        row = pos[1] // squareSize
        col = pos[0] // squareSize
        clicked_square = chess.square(col, 7 - row)

        # Nenhuma peça foi selecionada
        if self.selected_square is None:
            if self.board.piece_at(clicked_square) and self.board.piece_at(clicked_square).color == (self.board.turn):
                # Seleciona a peça
                self.selected_square = clicked_square
                pygame.draw.rect(
                    self.screen, 
                    pygame.Color(255, 255, 40), 
                    pygame.Rect(
                        col * squareSize, 
                        row * squareSize, 
                        squareSize, 
                        squareSize
                    )
                )

        # A mesma casa foi selecionada
        elif self.selected_square == clicked_square:
            self.draw_board()
            self.selected_square = None
            
        # Uma peça foi selecionada
        else:
            move = chess.Move(self.selected_square, clicked_square)

            # Verifica se é um caso de promoção
            if self.board.piece_at(self.selected_square).piece_type == chess.PAWN:
                if (
                    (self.board.turn == chess.WHITE and chess.square_rank(clicked_square) == 7) or 
                    (self.board.turn == chess.BLACK and chess.square_rank(clicked_square) == 0)
                ):
                    promotionPiece = promotion_event()

                    if (promotionPiece == 'q') or (promotionPiece == 'Q'):
                        move = chess.Move(self.selected_square, clicked_square, promotion=chess.QUEEN)
                    elif (promotionPiece == 'r') or (promotionPiece == 'R'):
                        move = chess.Move(self.selected_square, clicked_square, promotion=chess.ROOK)
                    elif (promotionPiece == 'b') or (promotionPiece == 'B'):
                        move = chess.Move(self.selected_square, clicked_square, promotion=chess.BISHOP)
                    elif (promotionPiece == 'n') or (promotionPiece == 'N'):
                        move = chess.Move(self.selected_square, clicked_square, promotion=chess.KNIGHT)

            if move in self.board.legal_moves:
                self.board.push(move)
            
            self.draw_board()
            
            self.selected_square = None
        self.draw_pieces(self.board)

    def verify_check(self):
        if self.board.is_check():
            # Obter a posição do rei que está em xeque
            if self.board.turn:
                king_square = self.board.king(chess.WHITE)
            else:
                king_square = self.board.king(chess.BLACK)

            # Destaca a posição do rei com uma cor vermelha
            row = 7 - (king_square // 8)
            col = king_square % 8
            pygame.draw.rect(
                self.screen, 
                pygame.Color(255, 0, 0), 
                pygame.Rect(
                    col * squareSize, 
                    row * squareSize, 
                    squareSize, 
                    squareSize
                )
            )
            self.draw_pieces(self.board)

    def has_ended(self) -> bool:
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                print("Black Wins!")
            else:
                print("White Wins!")
            return True
            
        elif (
            self.board.is_insufficient_material() or 
            self.board.is_stalemate() or 
            self.board.can_claim_threefold_repetition() or 
            self.board.can_claim_fifty_moves()
        ):
            print("Draw!")
            return True
        return False

    def playerVSbot(self, engine = Pyrarucu()):
        running = True

        self.draw_board()
        self.draw_pieces(self.board)

        while running:
            # Verificar se algum rei está em xeque
            self.verify_check()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.board.turn == chess.WHITE and event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_mouse_click(pos)
                elif self.board.turn == chess.BLACK:
                    result = engine.search(self.board)
                    self.board.push(result.move)
                    self.draw_board()
                    self.draw_pieces(self.board)

            # Verificar xeque-mate ou empate
            running = not self.has_ended()

    def botVSbot(self, engine1 = Pyrarucu(), engine2 = Pyrarucu()):
        running = True

        self.draw_board()
        self.draw_pieces(self.board)

        while running:
            # Verificar se algum rei está em xeque
            self.verify_check()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.board.turn == chess.WHITE:
                    result = engine1.search(self.board)
                    self.board.push(result.move)
                    time.sleep(0.5)
                elif self.board.turn == chess.BLACK:
                    result = engine2.search(self.board)
                    self.board.push(result.move)
                    time.sleep(0.5)
                self.draw_board()
                self.draw_pieces(self.board)

            # Verificar xeque-mate ou empate
            running = not self.has_ended()
