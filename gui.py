# importing required librarys
import pygame
import chess
import math
import chess.engine

#basic colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

PIECE_PATH = 'resources/pieces/'

class ChessGUI:
    def __init__(self, X: int = 640, Y: int = 640):
        self.X = X
        self.Y = Y
        self.screen = pygame.display.set_mode((self.X, self.Y))
        self.screen.fill(BLACK)
        self.pieces = {
            'p': pygame.image.load(PIECE_PATH + 'blackp.png').convert(),
            'n': pygame.image.load(PIECE_PATH + 'blackn.png').convert(),
            'b': pygame.image.load(PIECE_PATH + 'blackb.png').convert(),
            'r': pygame.image.load(PIECE_PATH + 'blackr.png').convert(),
            'q': pygame.image.load(PIECE_PATH + 'blackq.png').convert(),
            'k': pygame.image.load(PIECE_PATH + 'blackk.png').convert(),
            'P': pygame.image.load(PIECE_PATH + 'whitep.png').convert(),
            'N': pygame.image.load(PIECE_PATH + 'whiten.png').convert(),
            'B': pygame.image.load(PIECE_PATH + 'whiteb.png').convert(),
            'R': pygame.image.load(PIECE_PATH + 'whiter.png').convert(),
            'Q': pygame.image.load(PIECE_PATH + 'whiteq.png').convert(),
            'K': pygame.image.load(PIECE_PATH + 'whitek.png').convert(),
        }
        pygame.init()
        pygame.display.set_caption('Chess')

    def update(self, board):
        for i in range(64):
            piece = board.piece_at(i)
            if piece == None:
                pass
            else:
                self.screen.blit(self.pieces[str(piece)],((i%8)*80 + 10,570-(i//8)*80))
        
        for i in range(1, 8):
            pygame.draw.line(self.screen,WHITE,(0,i*80),(640,i*80))
            pygame.draw.line(self.screen,WHITE,(i*80,0),(i*80,640))
        
        pygame.display.flip()

    def get_index(self, mouse_pos):
        #find which square was clicked and index of it
        square = (math.floor(mouse_pos[0]/80),math.floor(mouse_pos[1]/80))
        index = (7-square[1])*8+(square[0])
        return index

    def play(self, board = chess.Board()):
        index_moves = []

        status = True
        while not board.is_game_over() and status is not False:
            #update screen
            self.update(board)
            for event in pygame.event.get():
        
                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    status = False

                # if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #remove previous highlights
                    self.screen.fill(BLACK)
                    #get position of mouse
                    pos = pygame.mouse.get_pos()
                    index = self.get_index(pos)
                    
                    # if we are moving a piece
                    if index in index_moves: 
                        move = moves[index_moves.index(index)]
                        board.push(move)
                        #reset index and moves
                        index = None
                        index_moves = []
                        
                        
                    # show possible moves
                    else:
                        #check the square that is clicked
                        piece = board.piece_at(index)
                        #if empty pass
                        if piece == None:
                            pass
                        else:
                            #figure out what moves this piece can make
                            all_moves = list(board.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    
                                    moves.append(m)

                                    t = m.to_square

                                    TX1 = 80*(t%8)
                                    TY1 = 80*(7-t//8)

                                    
                                    #highlight squares it can move to
                                    pygame.draw.rect(self.screen,BLUE,pygame.Rect(TX1,TY1,80,80),5)
                            
                            index_moves = [a.to_square for a in moves]
        
        # deactivates the pygame library
            if board.outcome() != None:
                print(board.outcome())
                status = False
                print(board)
        pygame.quit()

    def play_engine(self, engine, board = chess.Board()):
        index_moves = []

        status = True
        while not board.is_game_over() and status is not False:
            #update screen
            self.update(board)
            for event in pygame.event.get():
        
                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    status = False

                # if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #remove previous highlights
                    self.screen.fill(BLACK)
                    #get position of mouse
                    pos = pygame.mouse.get_pos()
                    index = self.get_index(pos)
                    
                    # if we are moving a piece
                    if index in index_moves: 
                        move = moves[index_moves.index(index)]
                        board.push(move)
                        result = engine.search(board)
                        board.push(result.move)
                        #reset index and moves
                        index = None
                        index_moves = []
                        
                        
                    # show possible moves
                    else:
                        #check the square that is clicked
                        piece = board.piece_at(index)
                        #if empty pass
                        if piece == None:
                            pass
                        else:
                            #figure out what moves this piece can make
                            all_moves = list(board.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    
                                    moves.append(m)

                                    t = m.to_square

                                    TX1 = 80*(t%8)
                                    TY1 = 80*(7-t//8)

                                    
                                    #highlight squares it can move to
                                    pygame.draw.rect(self.screen,BLUE,pygame.Rect(TX1,TY1,80,80),5)
                            
                            index_moves = [a.to_square for a in moves]
        
        # deactivates the pygame library
            if board.outcome() != None:
                print(board.outcome())
                status = False
                print(board)
        pygame.quit()
