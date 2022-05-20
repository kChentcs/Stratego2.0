import pygame

from Square import Square
from Pieces import Pieces
import random


class Board:
    def __init__(self, screen, x, y, row, column, sw, sh, bw, enemy = None):
        self.screen = screen
        self.x = x
        self.y = y
        self.row = row
        self.column = column
        self.squareWidth = sw
        self.squareHeight = sh
        self.borderWidth = bw
        self.enemy = enemy
        self.grid = []
        self.play = False
        self.selected = None
        self.enemyTurn = False
        self.endgame = False
        self.player1WON = False
        self.playerPieces = []
        self.enemyPieces = []
        self.piecePools = []
        self.draggables = []


        for i in range(column):
            newList = []
            for j in range(row):
                lake = (j == 4 or j == 5) and (i == 2 or i == 3 or i == 6 or i == 7)
                s = Square(i * (self.squareWidth) + self.x, j * (self.squareHeight) + self.y, self.squareWidth, self.squareHeight, self.borderWidth, self.screen, self, i, j, lake)
                newList.append(s)
            self.grid.append(newList)

    def update(self):
        for column in self.grid:
            for square in column:
                square.update()
        for pool in self.piecePools:
            pool.update()
        for drag in self.draggables:
            drag.update()
        if self.play:
            self.dead()
            if self.enemyTurn:
                self.enemy.makeMove()
                self.enemyTurn = False
        else:
            for pool in self.piecePools:
                if pool.numberpieces > 0:
                    return
            self.startGame()



    def handleEvent(self, event):
        for column in self.grid:
            for square in column:
                square.handleEvent(event)
        for pool in self.piecePools:
            pool.handleEvent(event)
        for drag in self.draggables:
            drag.handleEvent(event)

    def coordinatesToSquare(self, x, y):
        i = int((x - self.x)/self.squareWidth)
        j = int((y - self.y)/self.squareHeight)
        if i >= 0 and i < self.column and j >= 0 and j < self.row:
            #print("i = " + str(i) + " j =" + str(j))
            return self.grid[i][j]
        else:
            return None

    def autoFill(self):
        for column in self.grid:
            for square in column:
                if square.validatePlacement():
                    random.shuffle(self.piecePools)
                    for pool in self.piecePools:
                        if pool.numberpieces > 0:
                            piece = Pieces(square.sx, square.sy, pool.images, square, pool.name, pool)
                            square.piece = piece
                            pool.removePiece()
                            break

    def select(self, square):
        if self.selected:
            self.selected.selected = False
        if self.selected and self.selected.piece and self.selected.piece.validateMove(square):
            self.selected.piece.move(square)
            self.selected = None
            self.enemyTurn = True
        else:
            self.selected = square
            square.selected = True

    def die(self, piece):
        self.endgame = True
        self.player1WON = piece.enemy

    def dead(self):
        move = False
        if self.enemyTurn == False:
            pieceList = self.playerPieces
        else:
            pieceList = self.enemyPieces
        for piece in pieceList:
             validM = piece.getValidSquares(self.enemyTurn)
             if len(validM) > 0:
                move = True
                break
        if not move:
            self.endgame = True
            self.player1WON = self.enemyTurn

    def predict(self, piece, square):
        board = self.makeCopy()
        startSquare = board.coordinatesToSquare(piece.x, piece.y)
        newPiece = startSquare.piece
        targetSquare = board.coordinatesToSquare(square.sx, square.sy)
        if targetSquare.piece and targetSquare.piece.enemy != newPiece.enemy:
            newPiece.attack(targetSquare.piece)
        else:
            newPiece.move(targetSquare)
        return board

    def makeCopy(self):
        newBoard = Board(self.screen, self.x, self.y, self.row, self.column, self.squareWidth, self.squareHeight, self.borderWidth)
        newBoard.enemyTurn = self.enemyTurn
        for piece in self.playerPieces:
            newpiece = Pieces(piece.x, piece.y, None, newBoard.coordinatesToSquare(piece.x, piece.y), piece.name, None, piece.player, piece.enemy)
            newBoard.playerPieces.append(newpiece)
        for piece in self.enemyPieces:
            newpiece = Pieces(piece.x, piece.y, None, newBoard.coordinatesToSquare(piece.x, piece.y), piece.name, None, piece.player, piece.enemy)
            newBoard.enemyPieces.append(newpiece)

        return newBoard

    def startGame(self):
        self.play = True
        for pool in self.piecePools:
            pool.refill()
        self.enemy.placePieces()
        for i in self.grid:
            for j in i:
                square = j
                if square.piece:
                    if square.piece.enemy == False:
                        self.playerPieces.append(square.piece)
                    else:
                        self.enemyPieces.append(square.piece)

    def reset(self):
        for row in self.grid:
            for square in row:
                square.piece = None

        self.playerPieces = []
        self.enemyPieces = []

        for pool in self.piecePools:
            pool.refill()

        self.play = False
        self.endgame = False
        self.enemyTurn = False