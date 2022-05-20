import pygame
from Pieces import Pieces


class draggable:
    def __init__(self, screen, image, x, y, pieceName, piecePool):
        self.screen = screen
        self.image = image
        self.rect = image.get_rect()
        self.click = False
        self.startX = x
        self.startY = y
        self.rect.center = x, y
        self.piece = None
        self.pieceName = pieceName
        self.piecePool = piecePool
        self.board = piecePool.board

    def update(self):
        if self.click:
            self.rect.center = pygame.mouse.get_pos()
        self.screen.blit(self.image, self.rect)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.click = False
            mouseX, mouseY = event.pos
            square = self.board.coordinatesToSquare(mouseX, mouseY)
            if square and square.validatePlacement():
                self.piece = Pieces(mouseX, mouseY, self.image, square, self.pieceName, self.piecePool)
            else:
                self.piecePool.addPiece()
            self.board.draggables.remove(self)