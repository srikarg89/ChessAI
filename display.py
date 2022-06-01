import pygame
from helpers import *

WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
SQUARE_WIDTH = 68
PYGAME_DIMENSIONS = SQUARE_WIDTH * 8

class GUIDisplay:
    def __init__(self, board):
        self.board = board
        pygame.init()
        self.screen = pygame.display.set_mode((PYGAME_DIMENSIONS, PYGAME_DIMENSIONS))
        self.clock = pygame.time.Clock()
        self.dragging_info = None
    
    # Draw the image on an (x,y) location on the board
    def draw_img(self, x, y, filename):
        xcoord, ycoord = x * SQUARE_WIDTH, PYGAME_DIMENSIONS - (y * SQUARE_WIDTH) - SQUARE_WIDTH
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (SQUARE_WIDTH, SQUARE_WIDTH))
        self.screen.blit(img, (xcoord, ycoord))

    # Draw the image while its being dragged
    def draw_dragging_img(self):
        filename = get_filename(self.dragging_info[0])
        center = self.dragging_info[1], self.dragging_info[2]
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (SQUARE_WIDTH, SQUARE_WIDTH))
        self.screen.blit(img, (center[0] - SQUARE_WIDTH // 2, center[1] - SQUARE_WIDTH // 2))

    def set_board(self, board):
        self.board = board
        self.refresh()
    
    def draw_empty_board(self):
        self.screen.fill(WHITE)
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    pygame.draw.rect(self.screen, BLACK, pygame.Rect(i * SQUARE_WIDTH, PYGAME_DIMENSIONS - (j * SQUARE_WIDTH) - SQUARE_WIDTH, SQUARE_WIDTH, SQUARE_WIDTH))

    def refresh(self):
        self.draw_empty_board()
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece == 'e':
                    continue
                filename = get_filename(piece)
                self.draw_img(i, j, filename)

    def coord_to_idx(self, xcoord, ycoord):
        return int(xcoord / SQUARE_WIDTH), int((PYGAME_DIMENSIONS - ycoord) / SQUARE_WIDTH)

    # Returns a move if a move was made by the Human. Otherwise returns None
    def check_ui_action(self, current_turn):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    x, y = self.coord_to_idx(mouse_x, mouse_y)
                    piece = self.board[x][y]
                    if (current_turn == Color.WHITE and is_white(piece)) or (current_turn == Color.BLACK and is_black(piece)):
                        self.dragging_info = (piece, mouse_x, mouse_y, x, y)
                        self.board[x][y] = 'e'

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.dragging_info:
                        piece, xcoord, ycoord, oriX, oriY = self.dragging_info
                        x, y = self.coord_to_idx(xcoord, ycoord)
                        move = Move((oriX, oriY), (x, y), piece, None)
                        self.dragging_info = None
                        return move

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_info:
                    self.dragging_info = self.dragging_info[0], event.pos[0], event.pos[1], self.dragging_info[3], self.dragging_info[4]
        
        return None

    def render(self):
        self.refresh()
        if self.dragging_info:
            self.draw_dragging_img()
        pygame.display.update()
        self.clock.tick()

    def terminate(self):
        pygame.display.quit()
        pygame.quit()
