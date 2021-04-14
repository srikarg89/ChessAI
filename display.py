import pygame
from helpers import *

WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

class GUIDisplay:
    def __init__(self, game):
        self.game = game
        self.square_width = 68
        self.board = get_starting_board()
        pygame.init()
        self.dim = self.square_width * 8
        self.screen = pygame.display.set_mode((self.dim, self.dim))
        self.clock = pygame.time.Clock()
        self.dragging = None
        self.images = [[None for j in range(8)] for i in range(8)]
    
    def draw_img(self, x, y, filename):
        xcoord, ycoord = x * self.square_width, self.dim - (y * self.square_width) - self.square_width
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (self.square_width, self.square_width))
        self.images[x][y] = img
        self.screen.blit(img, (xcoord, ycoord))

    def draw_dragging_img(self):
        filename = get_filename(self.dragging[0])
        center = self.dragging[1], self.dragging[2]
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (self.square_width, self.square_width))
        xcoord = center[0] - self.square_width // 2
        ycoord = center[1] - self.square_width // 2
        self.screen.blit(img, (xcoord, ycoord))

    def set_board(self, board):
        self.board = board
        self.refresh()
    
    def draw_empty_board(self):
        self.screen.fill(WHITE)
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    pygame.draw.rect(self.screen, BLACK, pygame.Rect(i * self.square_width, self.dim - (j * self.square_width) - self.square_width, self.square_width, self.square_width))

    def refresh(self):
        self.draw_empty_board()
        self.images = [[None for j in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                piece = get_pos(self.board, i, j)
                if piece == 'e':
                    continue
                filename = get_filename(piece)
                self.draw_img(i, j, filename)

    def coord_to_idx(self, xcoord, ycoord):
        return int(xcoord / self.square_width), int((self.dim - ycoord) / self.square_width)

    def check_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.over = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    x, y = self.coord_to_idx(mouse_x, mouse_y)
                    piece = get_pos(self.board, x, y)
                    if (self.game.turn and is_white(piece)) or (not self.game.turn and is_black(piece)):
                        self.dragging = (piece, mouse_x, mouse_y, x, y)
                        place(self.board, x, y, 'e')

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.dragging:
                        piece, xcoord, ycoord, oriX, oriY = self.dragging
                        x, y = self.coord_to_idx(xcoord, ycoord)
                        move = Move((oriX, oriY), (x, y), piece, None)
                        self.game.make_move(move)
                        self.dragging = None

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    xcoord, ycoord = event.pos
                    self.dragging = self.dragging[0], xcoord, ycoord, self.dragging[3], self.dragging[4]

    def render(self):
        self.refresh()
        if self.dragging:
            self.draw_dragging_img()
        pygame.display.update()
        self.clock.tick()

    def terminate(self):
        pygame.display.quit()
        pygame.quit()

