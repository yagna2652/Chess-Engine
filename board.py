import pygame as p
from engine import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations
IMAGES = {}
p.display.set_caption("ChessBoard")

def load_images():
    pieces = ['wp', 'wR', 'wN','wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Gamestate()
    validMoves = gs.getValidMoves()
    movemade = False #flag variable for when move is made

    load_images()
    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user(tuple:(row,col))
    playerClicks = [] #keep track of the players clicks(two tuples)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected ==(row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0],playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        movemade = True

                    sqSelected = ()
                    playerClicks = []
                #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undomove()
                    movemade = True
        if movemade:
            validMoves = gs.getValidMoves()
            movemade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
def drawGameState(screen, gs):
    drawboard(screen)
    drawPieces(screen, gs.board)
def drawboard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def drawPieces(screen, board):
    for c in range(DIMENSION):
        for r in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
