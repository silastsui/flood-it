# Flood It
import random
import pygame
import sys

from pygame.locals import *

import colours
import settings


#start of main game loop
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((settings.WINDOWWIDTH, settings.WINDOWHEIGHT))

    myFont = pygame.font.SysFont("Calibri", 24)

    mousex, mousey = 0, 0

    pygame.display.set_caption("Flood It!")

    mainBoard = getRandomizedBoard(settings.ROWS, settings.COLUMNS, settings.ALLCOLOURS)
    floodBoard = [(0,0)]
    updatefloodBoard(mainBoard, floodBoard)
    lastColour = mainBoard[0][0]
    DISPLAYSURF.fill(settings.BGCOLOUR)
    pygame.draw.rect(DISPLAYSURF, settings.BORDERCOLOUR, (settings.XMARGIN, settings.YMARGIN, settings.COLUMNS * settings.BOXSIZE + settings.BOARDMARGIN * 2, settings.ROWS * settings.BOXSIZE + settings.BOARDMARGIN * 2))

    gameWon = myFont.render("Congratulations! You Won!", 1, BLACK)
    gameWon_Rect = gameWon.get_rect(center=(settings.WINDOWWIDTH/2, settings.WINDOWHEIGHT/8))

    #Main game loop
    while True:
        mouseClicked = False
        #Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        if mouseClicked == True:
            (xbox, ybox) = getBoxAtPixel(mousex, mousey)
            if xbox != None and ybox != None:
                updateBoard(mainBoard, floodBoard, xbox, ybox, lastColour)
                lastColour = mainBoard[ybox][xbox]

        if hasWon(mainBoard):
            DISPLAYSURF.blit(gameWon, gameWon_Rect)

        drawBoard(mainBoard)
        pygame.display.update()
        FPSCLOCK.tick(settings.FPS)


def getRandomizedBoard(ROWS, COLUMNS, colours):
    board = []
    for y in range(ROWS):
        board.append([])
        for x in range(COLUMNS):
            board[y].append(random.choice(colours))
    return board


def leftTopCoordsOfBox(xbox, ybox):
    left = settings.XMARGIN + settings.BOARDMARGIN + (xbox * settings.BOXSIZE)
    top = settings.YMARGIN + settings.BOARDMARGIN + (ybox * settings.BOXSIZE)
    return (left, top)


def getBoxAtPixel(xpos, ypos):
    xbox = (xpos - settings.XMARGIN - settings.BOARDMARGIN)/settings.BOXSIZE
    ybox = (ypos - settings.YMARGIN - settings.BOARDMARGIN)/settings.BOXSIZE
    if xbox < 0 or xbox >= settings.COLUMNS or ybox < 0 or ybox >= settings.ROWS:
        return (None, None)
    left, top = leftTopCoordsOfBox(xbox, ybox)
    boxRect = pygame.Rect(left, top, settings.BOXSIZE, settings.BOXSIZE)
    if boxRect.collidepoint(xpos, ypos):
        return (xbox, ybox)


def updateBoard(mainBoard, floodBoard, xbox, ybox, lastColour):
    fillColour = mainBoard[ybox][xbox]
    if fillColour == lastColour:
        return mainBoard
    fillInMainBoard(mainBoard, floodBoard, fillColour)
    updatefloodBoard(mainBoard, floodBoard)


def fillInMainBoard(mainBoard, floodBoard, fillColour):
    for item in floodBoard:
        mainBoard[item[0]][item[1]] = fillColour


def updatefloodBoard(mainBoard, floodBoard):
    board_changes = 1
    while board_changes != 0:
        board_changes = 0
        for y in range(settings.ROWS):
            for x in range(settings.COLUMNS):
                #this never passes
                if (y,x) not in floodBoard:
                    if checkAdjacentSquares(mainBoard, floodBoard, y, x):
                        board_changes += 1
                        floodBoard.append((y,x))
    return board_changes

#if x, y has a member of floodBoard beside it, return True
def checkAdjacentSquares(mainBoard, floodBoard, y, x):
    boxType = findBoxType(x,y)
    if boxType / 3 != 0:
        if mainBoard[y-1][x] == mainBoard[y][x] and (y-1, x) in floodBoard:
            return True
    if boxType / 3 != 2:
        if mainBoard[y+1][x] == mainBoard[y][x] and (y+1, x) in floodBoard:
            return True
    if boxType % 3 != 0:
        if mainBoard[y][x-1] == mainBoard[y][x] and (y, x-1) in floodBoard:
            return True
    if (boxType + 1) % 3 != 0:
        if mainBoard[y][x+1] == mainBoard[y][x] and (y, x+1) in floodBoard:
            return True
    return False

def findBoxType(x,y):
    if x == 0 and y == 0:
        return 0
    if x == settings.COLUMNS - 1 and y == 0:
        return 2
    if x == 0 and y == settings.ROWS - 1:
        return 6
    if x == settings.COLUMNS - 1 and y == settings.ROWS - 1:
        return 8
    if x == 0:
        return 3
    if y == 0:
        return 1
    if x == settings.COLUMNS - 1:
        return 5
    if y == settings.ROWS - 1:
        return 7
    return 4

def drawBoard(board):
    left = settings.XMARGIN + settings.BOARDMARGIN
    top = settings.YMARGIN + settings.BOARDMARGIN
    for xbox in range(settings.COLUMNS):
        for ybox in range(settings.ROWS):
            colour = board[ybox][xbox]
            pygame.draw.rect(DISPLAYSURF, colour, (left + xbox*settings.BOXSIZE, top + ybox*settings.BOXSIZE, settings.BOXSIZE, settings.BOXSIZE))

def hasWon(board):
    colour = board[0][0]
    for y in range(settings.ROWS):
        for x in range(settings.COLUMNS):
            if board[y][x] != colour:
                return False
    return True

if __name__ == '__main__':
    main()
