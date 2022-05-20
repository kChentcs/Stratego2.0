import math

import pygame
import random
from Pieces import Pieces
from Move import Move

class AI:
    def __init__(self, board, difficulty, isMax):
        self.board = board
        self.difficulty = difficulty
        self.setDifficulty(difficulty)
        self.isMax = isMax


    def placePieces(self):
        for column in self.board.grid:
            for square in column:
                if square.validatePlacement(True):
                    random.shuffle(self.board.piecePools)
                    for pool in self.board.piecePools:
                        if pool.numberpieces > 0:
                            piece = Pieces(square.sx, square.sy, pool.images, square, pool.name, pool, self, True)
                            square.piece = piece
                            pool.removePiece()
                            #self.board.enemyPieces.append(piece)
                            break

    def evaluateBoard(self, board):
        playerScore = 0
        enemyScore = 0
        for piece in board.playerPieces:
            # playerScore += piece.strength()
            playerScore += piece.values()
        for piece in board.enemyPieces:
            # enemyScore += piece.strength()
            enemyScore += piece.values()
        #print("black", blackScore)
        if self.isMax:
            return enemyScore - playerScore
        else:
            return playerScore - enemyScore

    # def maxi(self, depth, board, move):
    #     if depth == 0:
    #         move.score = self.evaluateBoard(board)
    #         return move
    #     max = -math.inf
    #     if self.isMax:
    #         pieces = board.enemyPieces
    #     else:
    #         pieces = board.playerPieces
    #     for piece in pieces:
    #         for move in piece.getValidSquares(True):
    #             testBoard = board.predict(piece, move)
    #             minMove = self.mini(depth - 1, testBoard, Move(piece, move))
    #             if minMove.score > max:
    #                 maxMove = minMove
    #     return maxMove
    #
    # def mini(self, depth, board, move):
    #     if depth == 0:
    #         move.score = -self.evaluateBoard(board)
    #         return move
    #     min = math.inf
    #     minMove = None
    #     if not self.isMax:
    #         pieces = board.enemyPieces
    #     else:
    #         pieces = board.playerPieces
    #     for piece in pieces:
    #         for move in piece.getValidSquares(True):
    #             testBoard = board.predict(piece, move)
    #             maxMove = self.maxi(depth - 1, testBoard, Move(piece, move))
    #             if maxMove.score < min:
    #                 minMove = maxMove
    #     return minMove


    def miniMax(self, board, depth, isMax):
        if depth == 0:
            return self.evaluateBoard(board)
        if isMax:
            value = -math.inf
            if self.isMax:
                pieces = board.enemyPieces
                enemyMove = True
                board.enemyMove = True
            else:
                pieces = board.playerPieces
                enemyMove = False
                board.enemyMove = False
            for piece in pieces:
                for move in piece.getValidSquares(enemyMove):
                    testBoard = board.predict(piece, move)
                    value = max(value, self.miniMax(testBoard, depth - 1, False))
        else:
            value = math.inf
            if not self.isMax:
                pieces = board.enemyPieces
                enemyMove = True
                board.enemyMove = True
            else:
                pieces = board.playerPieces
                enemyMove = False
                board.enemyMove = False
            for piece in pieces:
                for move in piece.getValidSquares(enemyMove):
                    testBoard = board.predict(piece, move)
                    value = min(value, self.miniMax(testBoard, depth - 1, True))

        return value

    def makeMove(self):
        bestMove = None
        bestMovePiece = None
        if self.isMax:
            bestMoveScore = -math.inf
        else:
            bestMoveScore = math.inf
        for piece in self.board.enemyPieces:
            for move in piece.getValidSquares(True):
                testBoard = self.board.predict(piece, move)
                score = self.miniMax(testBoard, self.depth, self.isMax)
                if (self.isMax and score > bestMoveScore) or (not self.isMax and score < bestMoveScore):
                    bestMove = move
                    bestMovePiece = piece
                    bestMoveScore = score
                print(score)

        print("bestmovescore: ", bestMoveScore)
        bestMovePiece.move(bestMove)

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        if self.difficulty == "Easy":
            self.depth = 2
        if self.difficulty == "Medium":
            self.depth = 3
        if self.difficulty == "Hard":
            self.depth = 4