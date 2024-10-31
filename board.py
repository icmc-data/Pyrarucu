# Interface Gráfica do Tabuleiro de Xadrez (GUI)
# Permite escolher entre os seguintes modos: player (brancas) vs bot e bot vs bot

import chess
import chess.engine
import pygame
import time
from strategies import RandomMove

pygame.init()
board = chess.Board()

# Definições de dimensões, cores e fonte
width, height = 640, 640
squareSize = width // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
FONT = pygame.font.Font(None, 36)

# screen é uma janela gráfica com dimensões width e height
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Board")

def DrawBoard():
    colors = [WHITE, GRAY]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            # Desenha um retângulo/tabuleiro
            pygame.draw.rect(screen, color, pygame.Rect(col * squareSize, row * squareSize, squareSize, squareSize))

def DrawPieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = pygame.image.load(f"images/{piece.symbol()}.png")
            row = 7 - (square // 8)
            col = square % 8
            # Sobrepõe a imagem da peça sobre o tabuleiro
            screen.blit(piece_image, pygame.Rect(col * (squareSize) + 8, row * (squareSize) + 10, squareSize, squareSize))

def DrawModeSelectionScreen(screen):
    pygame.draw.rect(screen, GRAY, (200, 100, 240, 50))
    pygame.draw.rect(screen, GRAY, (200, 160, 240, 50))

    text_botPlayer = FONT.render("Player vs Bot", True, WHITE)
    text_doubleBot = FONT.render("Bot vs Bot", True, WHITE)
    screen.blit(text_botPlayer, (237, 110))
    screen.blit(text_doubleBot, (255, 170))

    # Atualiza a tela
    pygame.display.flip()
    
def PromotionEvent():
    pygame.draw.rect(screen, (255, 255, 60), pygame.Rect(width // 4, height // 4, width // 2, height // 8))

    optionsWhite = ['Q', 'R', 'B', 'N']
    optionsBlack = ['q', 'r', 'b', 'n']

    if board.turn == chess.WHITE:
        final = optionsWhite
    else:
        final = optionsBlack

    # Insere na tela as peças de promoção corretas
    for i, piece in enumerate(final):
        piece_image = pygame.image.load(f"images/{final[i]}.png")
        screen.blit(piece_image, pygame.Rect((width // 4) + i * (squareSize + 5), height // 4, squareSize, squareSize))

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

selected_square = None  # Quadrado inicial da peça selecionada

# Define o controle das ações e movimentos ao clicar com o mouse
def handle_mouse_click(pos):
    global selected_square
    row = pos[1] // squareSize
    col = pos[0] // squareSize
    clicked_square = chess.square(col, 7 - row)

    # Nenhuma peça foi selecionada ainda
    if selected_square is None:
        if board.piece_at(clicked_square) and board.piece_at(clicked_square).color == (board.turn):
            # Seleciona a peça
            selected_square = clicked_square
    # Uma peça foi selecionada
    else:
        move = chess.Move(selected_square, clicked_square)

        # Verifica se é um caso de promoção
        if board.piece_at(selected_square).piece_type == chess.PAWN:
            if (board.turn == chess.WHITE and chess.square_rank(clicked_square) == 7) or (board.turn == chess.BLACK and chess.square_rank(clicked_square) == 0):
                promotionPiece = PromotionEvent()

                if (promotionPiece == 'q') or (promotionPiece == 'Q'):
                    move = chess.Move(selected_square, clicked_square, promotion=chess.QUEEN)
                elif (promotionPiece == 'r') or (promotionPiece == 'R'):
                    move = chess.Move(selected_square, clicked_square, promotion=chess.ROOK)
                elif (promotionPiece == 'b') or (promotionPiece == 'B'):
                    move = chess.Move(selected_square, clicked_square, promotion=chess.BISHOP)
                elif (promotionPiece == 'n') or (promotionPiece == 'N'):
                    move = chess.Move(selected_square, clicked_square, promotion=chess.KNIGHT)

        if move in board.legal_moves:
            board.push(move)

        selected_square = None

def playerVSbot():
    engine = RandomMove()
    running = True
    clickedSquare = None

    while running:
        DrawBoard()

        # Verificar se algum rei está em xeque
        if board.is_check():
            # Obter a posição do rei que está em xeque
            if board.turn:
                king_square = board.king(chess.WHITE)
            else:
                king_square = board.king(chess.BLACK)

            # Destaca a posição do rei com uma cor vermelha
            row = 7 - (king_square // 8)
            col = king_square % 8
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), pygame.Rect(col * squareSize, row * squareSize, squareSize, squareSize))

        # Destaca a posição clicada pelo jogador em amarelo
        if (clickedSquare != None) and (board.turn == chess.WHITE):
            row, col = clickedSquare
            if (board.piece_at(chess.square(col, 7 - row))):
                pygame.draw.rect(screen, pygame.Color(255, 255, 40), pygame.Rect(col * squareSize, row * squareSize, squareSize, squareSize))

        DrawPieces(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif board.turn == chess.WHITE and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // squareSize
                row = (pos[1] // squareSize)
                clickedSquare = (row, col)

                handle_mouse_click(pos)
            elif board.turn == chess.BLACK:
                result = engine.search(board)
                board.push(result.move)
                
        # Verificar xeque-mate ou empate
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                print("Black Wins!")
            else:
                print("White Wins!")
            running = False
            
        elif board.is_insufficient_material() or board.is_stalemate() or board.can_claim_threefold_repetition() or board.can_claim_fifty_moves():
            print("Draw!")
            running = False


def botVSbot():
    running = True
    engine = RandomMove()

    while running:
        DrawBoard()

        # Verificar se algum rei está em xeque
        if board.is_check():
            # Obter a posição do rei que está em xeque
            if board.turn:
                king_square = board.king(chess.WHITE)
            else:
                king_square = board.king(chess.BLACK)

            # Destaca a posição do rei com uma cor vermelha
            row = 7 - (king_square // 8)
            col = king_square % 8
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), pygame.Rect(col * squareSize, row * squareSize, squareSize, squareSize))

        DrawPieces(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        result = engine.search(board)
        board.push(result.move)

        time.sleep(0.5)

        # Verificar xeque-mate ou empate
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                print("White Wins!")
            else:
                print("Black Wins!")
            running = False

        elif board.is_insufficient_material() or board.is_stalemate() or board.can_claim_threefold_repetition() or board.can_claim_fifty_moves():
            print("Draw!")
            running = False

def main():
    clock = pygame.time.Clock()
    mode = None

    DrawModeSelectionScreen(screen)

    # Escolha do modo de jogo
    while True:
        if mode != None:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 200 <= x <= 440 and 100 <= y <= 150:
                    mode = "p-bot"
                elif 200 <= x <= 440 and 160 <= y <= 210:
                    mode = "bot-bot"

    if mode == "p-bot":
        playerVSbot()
    else:
        botVSbot()

    pygame.quit()

if __name__ == "__main__":
    print("Iniciando jogo de xadrez")
    main()
