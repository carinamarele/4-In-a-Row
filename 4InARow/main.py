import pygame, sys
import random, copy
from pygame.locals import *


#importare imagini necesare pentru meniul principal cand se joaca cu computerul
TITLE=pygame.image.load('tile.png')
GAMEIMG=pygame.image.load('game.png')
BACKGROUND=pygame.image.load('bk.png')

EASYIMG=pygame.image.load('easy.png')
MEDIUMIMG=pygame.image.load('medium.png')
HARDIMG=pygame.image.load('hard.png')

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('4 In A Row')
screen = pygame.display.set_mode((950, 800), 0, 32)

font = pygame.font.SysFont('Comic Sans MS', 50)

WINDOWWIDTH = 950 # lungimea ferestrei,in pixeli
WINDOWHEIGHT = 800 # inaltime fereastra in pixeli
BOARDWIDTH = int(sys.argv[2])  # cat de lunga este tabla
BOARDHEIGHT = int(sys.argv[3])  # cat de inalta este tabla

pygame.display.set_icon(GAMEIMG)

display_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
NEXTHUMAN = 'next'
COMPUTER = 'computer'

class Button():
    def __init__(self,x,y,image,scale):
        width=image.get_width()
        height=image.get_height()

        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))


def main_menu(oponent):
    while True:
        display_surface.blit(BACKGROUND, (0, 0))
        mx, my = pygame.mouse.get_pos()
        x=WINDOWWIDTH*0.02+30
        y=WINDOWHEIGHT*0.2-120
        display_surface.blit(TITLE, (x, y - 10))
        display_surface.blit(GAMEIMG, (x, y + 100))

        #se va alege dificultatea cand se joaca impotriva calculatorului
        if oponent==COMPUTER:

            button_1 = pygame.Rect(655, 230, 185, 50)
            button_2 = pygame.Rect(655, 380, 185, 50)
            button_3 = pygame.Rect(655, 520, 185, 50)

            easy_button = Button(600, 100, EASYIMG, 0.5)
            medium_button = Button(600, 250, MEDIUMIMG, 0.5)
            hard_button = Button(600, 400, HARDIMG, 0.5)
            pygame.draw.rect(screen, (255, 0, 0), button_1)
            pygame.draw.rect(screen, (255, 0, 0), button_2)
            pygame.draw.rect(screen, (254, 0, 0), button_3)
            easy_button.draw()
            medium_button.draw()
            hard_button.draw()

            if button_1.collidepoint((mx, my)):
                if click:
                   startGame(oponent, 1)
            if button_2.collidepoint((mx, my)):
                if click:
                   startGame(oponent, 2)
            if button_3.collidepoint((mx, my)):
                if click:
                   startGame(oponent, 3)
        else:
            #VS Human
            startGame(oponent, 0)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


SPACESIZE = 50 #dimensiunea tokenurilor

FPS = 30 # frames per second to update the screen



#pozitia de unde incepe tabla
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)


def startGame(oponent, dificulty):

    global FPSCLOCK, SHOWSURFACE, REDPILERECT, BLACKPILERECT
    global BLACKTOKENIMG, REDTOKENIMG, BOARDIMG, HUMANWINNERIMG, HUMAN1WINNERIMG, HUMAN2WINNERIMG, COMPUTERWINNERIMG, WINNERRECT, TIEIMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SHOWSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


    #setarea bilelor langa tabla de joc(pe de o parte si de alta a ei), folosim rect pentru a putea apasa pe ele
    REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE,
                                SPACESIZE)

    # modific imaginea la o dimensiune potrivita
    BOARDIMG = pygame.image.load('board.png')
    BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))
    REDTOKENIMG = pygame.image.load('token_red.png')
    REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
    BLACKTOKENIMG = pygame.image.load('token_black.png')
    BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))


    HUMANWINNERIMG = pygame.image.load('human_winner.png')
    HUMAN1WINNERIMG = pygame.image.load('human1_winner.png')
    HUMAN2WINNERIMG = pygame.image.load('human2_winner.png')
    COMPUTERWINNERIMG = pygame.image.load('computer_winner.png')
    TIEIMG = pygame.image.load('tie.png')

    WINNERRECT = HUMANWINNERIMG.get_rect()
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    isFirstGame = True
    while True:
        if oponent=='computer':
          runGame(isFirstGame,dificulty)
          isFirstGame = False
        else:
            #Human VS Human
            runGameHumans(isFirstGame)
            isFirstGame = False

def runGameHumans(isFirstGame):

    #cand se deschide aplicatia, se presupune ca primul jucator stie cum se muta piesele si de aceea va muta el primul
    if isFirstGame:
        turn = HUMAN
    else:
        # Altfel se alege random cine incepe
        if random.randint(0, 1) == 0:
            turn = NEXTHUMAN
        else:
            turn = HUMAN


    # Construim noua tabla de joc
    mainBoard = getNewBoard()

    while True:
        # loop-ul principal unde se decide ce se va face in functie de tura
        #Human primul jucator(RED), NEXTHUMAN al doilea(BLACK)

        if turn == HUMAN:
            getHumanMove(mainBoard)

            #dupa fiecare mutare se verifica daca a castigat si se afiseaza imaginea corespunzatoare
            if isWinner(mainBoard, RED):
                winnerImg = HUMAN1WINNERIMG
                break
            #dupa ce face mutarea, tura se muta la celalalt jucator
            turn = NEXTHUMAN

        else: #al doilea jucator

            getNextHumanMove(mainBoard)
            if isWinner(mainBoard, BLACK):
                winnerImg = HUMAN2WINNERIMG
                break

            turn = HUMAN # si revenim inapoi la primul jucator dupa mutare


       # daca ajungem in cazul in care nu mai avem unde muta inseamna ca este remiza si se va afisa mesajul corespunzator
        if isBoardFull(mainBoard):
            winnerImg = TIEIMG
            break

    while True:
        # Keep looping until player clicks the mouse or quits.
        drawBoard(mainBoard)
        SHOWSURFACE.blit(winnerImg, WINNERRECT)

        FPSCLOCK.tick()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return
        pygame.display.update()


def runGame(isFirstGame,dificulty):
    if isFirstGame:
        #HUMAN(RED) , COMPUTER(BLACK)
       #in jocul impotriva calculatorului, acesta va muta primul la primul joc pentru a vedea cum se muta
        turn = COMPUTER
    else:
        # altfel alegem random
        if random.randint(0, 1) == 0:
            turn = COMPUTER
        else:
            turn = HUMAN


    # Contruim noua tabla de joc
    mainBoard = getNewBoard()

    while True:
        if turn == HUMAN:

            getHumanMove(mainBoard)

            if isWinner(mainBoard, RED):
                winnerImg = HUMANWINNERIMG
                break

            turn = COMPUTER
        else:
            #COMPUTER MOVE
            if isWinner(mainBoard, BLACK):
                winnerImg = COMPUTERWINNERIMG
                break

            turn = HUMAN

        if isBoardFull(mainBoard):
            winnerImg = TIEIMG
            break

    while True:
        drawBoard(mainBoard)
        SHOWSURFACE.blit(winnerImg, WINNERRECT)
        FPSCLOCK.tick()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return

        pygame.display.update()

#pozitionez bila pentru un player pe coloana dorita si pe cel mai jos rand
def makeMove(board, player, column):
    lowest = getLowestEmptySpace(board, column)
    if lowest != -1:
        board[column][lowest] = player

#desenez tabla, extraToken reprezinta locul unde va fi pusa bila
def drawBoard(board, extraToken=None):

    #initial pun extraToken=none pentru cand desenez tabla la inceperea jocului, inainte de vreo mutare
    display_surface.blit(BACKGROUND, (0, 0))

    # desenez tokenurile,verificand daca in board am RED sau BLACK
    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            if board[x][y] == RED:#afisez imaginea corespunzatoare
                SHOWSURFACE.blit(REDTOKENIMG, spaceRect)
            elif board[x][y] == BLACK:
                SHOWSURFACE.blit(BLACKTOKENIMG, spaceRect)

    # desenez tokenul pe care il vreau sa il pun, adica cand fac mutare
    if extraToken != None:
        if extraToken['color'] == RED:
            SHOWSURFACE.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
        elif extraToken['color'] == BLACK:
            SHOWSURFACE.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

    # desenez imaginea pentru tabla
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            SHOWSURFACE.blit(BOARDIMG, spaceRect)

    # desenez locul de unde iau bilele
    SHOWSURFACE.blit(REDTOKENIMG, REDPILERECT) # red on the left
    SHOWSURFACE.blit(BLACKTOKENIMG, BLACKPILERECT) # black on the right

#construiesc tabla intr-un array(structura tablei)
def getNewBoard():
    board = []
    for x in range(BOARDWIDTH):
        board.append([EMPTY] * BOARDHEIGHT)
    return board


def getHumanMove(board):
    draggingToken = False
    tokenx, tokeny = None, None

    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #verific daca se apasa pe imaginea de unde trebuie sa iau bilele si memorez pozitia
            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos):
                draggingToken = True
                tokenx, tokeny = event.pos

            #memorez pozitia actuala cand mouse ul se misca
            elif event.type == MOUSEMOTION and draggingToken:
                tokenx, tokeny = event.pos

            #dau drumul obiectului si verific daca are pozitia in intervalul corespunzator tablei
            elif event.type == MOUSEBUTTONUP and draggingToken:

                #daca nu depaseste tabla, verific daca pot efectua miscare si daca da apelez animatia si actualizez tabla si redesenez
                if tokeny < YMARGIN and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN:
                    column = int((tokenx - XMARGIN) / SPACESIZE)

                    if isValidMove(board, column):
                        animateDroppingToken(board, column, RED)
                        board[column][getLowestEmptySpace(board, column)] = RED
                        drawBoard(board)
                        pygame.display.update()
                        return

                #sterg pozitiile memorate anterior pentru urmatoarea miscare
                tokenx, tokeny = None, None
                draggingToken = False

        #daca tokenx si tokeny raman goale atunci tabla ramane neschimbata, altfel o redesnez cu mutarea efectuata
        if tokenx != None and tokeny != None:
            drawBoard(board, {'x':tokenx - int(SPACESIZE / 2), 'y':tokeny - int(SPACESIZE / 2), 'color':RED})
        else:
            drawBoard(board)


        pygame.display.update()
        FPSCLOCK.tick()


#la fel ca la primul jucator
def getNextHumanMove(board):

    draggingToken = False

    tokenx = None
    tokeny = None

    while True:
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN and not draggingToken and BLACKPILERECT.collidepoint(event.pos):
                draggingToken = True
                tokenx, tokeny = event.pos

            elif event.type == MOUSEMOTION and draggingToken:
                tokenx, tokeny = event.pos

            elif event.type == MOUSEBUTTONUP and draggingToken:

                if tokeny > (YMARGIN - SPACESIZE) and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN:

                    column = int((tokenx - XMARGIN) / SPACESIZE)
                    if isValidMove(board, column):
                        animateDroppingToken(board, column, BLACK)
                        board[column][getLowestEmptySpace(board, column)] = BLACK
                        drawBoard(board)
                        pygame.display.update()
                        return
                tokenx, tokeny = None, None
                draggingToken = False

        if tokenx != None and tokeny != None:
            drawBoard(board, {'x':tokenx-int(SPACESIZE / 2) , 'y':tokeny-int(SPACESIZE / 2) , 'color':BLACK})
        else:
            drawBoard(board)

        pygame.display.update()
        FPSCLOCK.tick()


# animatia pentru mutare, am nevoie de tabla cu pozitiile ocupate, de pozitia(din lungime) unde vreau sa fac mutarea si culoarea tokenului
def animateDroppingToken(board, column, color):

    #calculez pozitia in pixeli pe tabla
    x = XMARGIN + column * SPACESIZE
    y = YMARGIN - SPACESIZE

    dropSpeed = 1.0

    #decid unde voi pune bila(din cele mai joase locuri libere)
    lowestEmptySpace = getLowestEmptySpace(board, column)

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.5

        #cat timp nu ajung la pozitia unde vreau sa pun, bila cade.
        if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
            return
        drawBoard(board, {'x':x, 'y':y, 'color':color})
        pygame.display.update()
        FPSCLOCK.tick()


#returnez indicele randului pentru cel mai jos spatiu liber de pe coloana data
#daca nu mai este loc va returna -1
def getLowestEmptySpace(board, column):
    for y in range(BOARDHEIGHT-1, -1, -1):# start,stop,step
        if board[column][y] == EMPTY:
            return y
    return -1


#verific daca a depasit bordura tablei sau daca locul unde vreau sa pun e ocupat
def isValidMove(board, column):
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        return False
    return True

#verific daca mai este vreun loc liber
def isBoardFull(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True

#iau pe cazuri, tile={RED,BLACK}
def isWinner(board, tile):
    # verific orizontal
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
    # verific vertical
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True
    # verific diagonal(\)
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True
    # verific diagonal(/)
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False


if __name__ == "__main__":

    OPONENT = sys.argv[1]
    WIDTH = int(sys.argv[2])
    LENGHT= int(sys.argv[3])
    main_menu(OPONENT)
