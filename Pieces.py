import pygame
import math

class Pieces:
    def __init__(self, x, y, image, square, name, piecePool, player = None, enemy = False):
        self.x = x
        self.y = y
        self.image = image
        self.square = square
        if square:
            self.square.piece = self
        self.name = name
        self.enemy = enemy
        self.piecePool = piecePool
        self.revealed = True
        self.player = player

    def move(self, square):
        if square.piece:
            self.attack(square.piece)

        else:
            if self.square:
                self.square.piece = None
            self.square = square
            self.square.piece = self

    def validateMove(self, square, enemyMove = False):
        if self.enemy and not enemyMove:
            return False
        if square.piece and enemyMove == square.piece.enemy:
            return False
        if square.lake:
            return False
        xdiff = abs(self.square.gridX - square.gridX)
        ydiff = abs(self.square.gridY - square.gridY)
        if not (xdiff == 1 or ydiff == 1) and not self.name == "scout":
            return False
        if not (self.square.sx == square.sx or self.square.sy == square.sy):
            return False
        if self.name == "flag" or self.name == "bomb":
            return False
        if self.name == "scout":
            if self.square.gridX > square.gridX and ydiff == 0:
                for i in range(self.square.gridX - 1, square.gridX, -1):
                    if square.board.grid[i][square.gridY].piece or not self.validateMove(square.board.grid[i][square.gridY], enemyMove):
                        return False
            elif self.square.gridX < square.gridX and ydiff == 0:
                for i in range(self.square.gridX + 1, square.gridX, 1):
                    if square.board.grid[i][square.gridY].piece or not self.validateMove(square.board.grid[i][square.gridY], enemyMove):
                        return False
            elif self.square.gridY > square.gridY and xdiff == 0:
                for i in range(self.square.gridY - 1, square.gridY, -1):
                    if square.board.grid[square.gridX][i].piece or not self.validateMove(square.board.grid[square.gridX][i], enemyMove):
                        return False
            elif self.square.gridY < square.gridY and xdiff == 0:
                for i in range(self.square.gridY + 1, square.gridY, 1):
                    if square.board.grid[square.gridX][i].piece or not self.validateMove(square.board.grid[square.gridX][i], enemyMove):
                        return False
            else:
                return False
        return True

    def getValidSquares(self, enemyMove):
        validMove = []
        for column in self.square.board.grid:
            for square in column:
                if self.validateMove(square, enemyMove):
                    validMove.append(square)
        return validMove

    # def strength(self):
    #     if self.name == "flag":
    #         return 0
    #     elif self.name == "spy":
    #         return 1
    #     elif self.name == "scout":
    #         return 2
    #     elif self.name == "miner":
    #         return 3
    #     elif self.name == "sergeant":
    #         return 4
    #     elif self.name == "lieutenant":
    #         return 5
    #     elif self.name == "captain":
    #         return 6
    #     elif self.name == "major":
    #         return 7
    #     elif self.name == "colonel":
    #         return 8
    #     elif self.name == "general":
    #         return 9
    #     elif self.name == "marshal":
    #         return 10
    #     elif self.name == "bomb":
    #         return 11
    #     else:
    #         return -1

    def values(self):
        if self.name == "flag":
            return 100
        elif self.name == "spy":
            return 1
        elif self.name == "scout":
            return 2
        elif self.name == "miner":
            return 3
        elif self.name == "sergeant":
            return 4
        elif self.name == "lieutenant":
            return 5
        elif self.name == "captain":
            return 6
        elif self.name == "major":
            return 7
        elif self.name == "colonel":
            return 8
        elif self.name == "general":
            return 9
        elif self.name == "marshal":
            return 10
        elif self.name == "bomb":
            return 0
        else:
            return -1


    def attack(self, enemyPiece):
        self.revealed = True
        enemyPiece.revealed = True
        if self.values() >= enemyPiece.values() or \
                (self.name == "miner" and enemyPiece.name == "bomb") or (self.name == "spy" and enemyPiece.name == "marshal") or \
                (self.name == "spy" and enemyPiece.name == "flag") or (self.name == "scout" and enemyPiece.name == "flag") or \
                (self.name == "miner" and enemyPiece.name == "flag") or (self.name == "sergeant" and enemyPiece.name == "flag") or \
                (self.name == "lieutenant" and enemyPiece.name == "flag") or (self.name == "captain" and enemyPiece.name == "flag") or \
                (self.name == "major" and enemyPiece.name == "flag") or (self.name == "colonel" and enemyPiece.name == "flag") or \
                (self.name == "general" and enemyPiece.name == "flag") or (self.name == "marshal" and enemyPiece.name == "flag"):
            if enemyPiece.piecePool:
                enemyPiece.piecePool.addPiece()
            enemyPiece.square.piece = None
            self.move(enemyPiece.square)
            if enemyPiece.enemy:
                self.square.board.enemyPieces.remove(enemyPiece)
            if enemyPiece.name == "flag":
                self.square.board.die(enemyPiece)
        else:

            if self.enemy:
                # self.player.pieces.remove(self)
                self.square.board.enemyPieces.remove(self)
            else:
                self.square.board.playerPieces.remove(self)
            self.square.piece = None
            self.square = None



