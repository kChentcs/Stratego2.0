import pygame
pygame.init()

from Screen import Screen
from textButton import textButton
from TextLabel import TextLabel
from PiecePool import PiecePool
from Board import Board
from AI import AI

screen = pygame.display.set_mode((900, 1000))
pygame.display.set_caption("Stratego")
Menufont = pygame.font.Font("Fonts/BungeeInline-Regular.ttf",100)
TextFont = pygame.font.Font("Fonts/Cinzel-VariableFont_wght.ttf",20)


boardbg = pygame.image.load("Images/Stratego Board.JPG")
boardbg = pygame.transform.scale(boardbg, (900, 900))
scout = pygame.transform.scale(pygame.image.load("Images/stratego-scout.png"), (80, 80))
captain = pygame.transform.scale(pygame.image.load("Images/stratego-captain.png"), (80,80))
bomb = pygame.transform.scale(pygame.image.load("Images/stratego-bomb.png"), (80,80))
colonel = pygame.transform.scale(pygame.image.load("Images/stratego-colonel.png"), (80,80))
flag = pygame.transform.scale(pygame.image.load("Images/stratego-flag.png"), (80,80))
general = pygame.transform.scale(pygame.image.load("Images/stratego-general.png"), (80,80))
lieutenant = pygame.transform.scale(pygame.image.load("Images/stratego-lieutenant.png"), (80,80))
major = pygame.transform.scale(pygame.image.load("Images/stratego-major.png"), (80,80))
marshal = pygame.transform.scale(pygame.image.load("Images/stratego-marshal.png"), (80,80))
miner = pygame.transform.scale(pygame.image.load("Images/stratego-miner.png"), (80,80))
spy = pygame.transform.scale(pygame.image.load("Images/stratego-spy.png"), (80,80))
sergeant = pygame.transform.scale(pygame.image.load("Images/stratego-sergeant.png"), (80,80))


def setupPiecePools(board):
    flagPool = PiecePool(1, flag, 40, 910, screen, TextFont, "flag", board)
    spyPool = PiecePool(1, spy, 200, 910, screen, TextFont, "spy", board)
    scoutPool = PiecePool(8, scout, 280, 910, screen, TextFont, "scout", board)
    minerPool = PiecePool(5, miner, 345, 910, screen, TextFont, "miner", board)
    sergeantPool = PiecePool(4, sergeant, 415, 910, screen, TextFont, "sergeant", board)
    lieutenantPool = PiecePool(4, lieutenant, 490, 910, screen, TextFont, "lieutenant", board)
    captainPool = PiecePool(4, captain, 560, 910, screen, TextFont, "captain", board)
    majorPool = PiecePool(3, major, 620, 910, screen, TextFont, "major", board)
    colonelPool = PiecePool(2, colonel, 685, 910, screen, TextFont, "colonel", board)
    generalPool = PiecePool(1, general, 740, 910, screen, TextFont, "general", board)
    marshalPool = PiecePool(1, marshal, 820, 910, screen, TextFont, "marshal", board)
    bombPool = PiecePool(6, bomb, 120, 900, screen, TextFont, "bomb", board)


board = Board(screen, 47, 50, 10, 10, 80, 80, 1)
AIplayer = AI(board, "Easy", False)
board.enemy = AIplayer
setupPiecePools(board)

playButton = textButton(lambda: switchScreen(AIDifficultyScreen), screen, "play", 390, 540, 100, 60, TextFont)
TitleText = TextLabel(screen, "Stratego", 450, 200, 200, 100, Menufont, centered = True)
menuScreen = Screen(screen, [playButton, TitleText], [playButton], (18, 165, 175))

AIEasy = textButton([lambda: switchScreen(setupScreen), lambda: AIplayer.setDifficulty("Easy")], screen, "Easy", 390, 400, 100, 60, TextFont)
AIMedium = textButton([lambda: switchScreen(setupScreen), lambda: AIplayer.setDifficulty("Medium")], screen, "Medium", 390, 500, 100, 60, TextFont)
AIHard = textButton([lambda: switchScreen(setupScreen), lambda: AIplayer.setDifficulty("Hard")], screen, "Hard", 390, 600, 100, 60, TextFont)
AIDifficultyScreen = Screen(screen, [AIEasy, AIMedium, AIHard, TitleText], [AIEasy, AIMedium, AIHard], (18, 165, 175))

autofillB = textButton(lambda: board.autoFill(), screen, "autofill", 400, 850, 80, 40, TextFont)
setupScreen = Screen(screen, [board, autofillB], [board, autofillB], (0, 0, 255), boardbg)

playAgain = textButton(lambda: switchScreen(menuScreen), screen, "Play Again", 390, 400, 130, 60, TextFont)
gameOverText = TextLabel(screen, "Game Over", 450, 200, 150, 75, Menufont, centered = True, tc = (255, 255, 255))
winnerText = TextLabel(screen, " team wins!", 450, 300, 100, 50, TextFont, centered = True, tc = (255, 255, 255))
endGameScreen = Screen(screen, [playAgain, gameOverText, winnerText], [playAgain], (0, 0, 0))

currentScreen = menuScreen

done = False

def switchScreen(newScreen):
    global currentScreen
    if newScreen == None:
        return
    currentScreen = newScreen


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        currentScreen.handleEvent(event)
    currentScreen.update()
    if board.endgame:
        winner = "blue" if board.player1WON else "red"
        winnerText.setText(winner + " team wins!")
        currentScreen = endGameScreen
        board.reset()
    pygame.display.flip()
pygame.quit()